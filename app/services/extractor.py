import pytesseract
from typing import Optional
from pdf2image import convert_from_path
from pypdf import PdfReader
from pathlib import Path
from PIL import Image
from dataclasses import dataclass
from datetime import datetime
import pandas as pd
import hashlib


@dataclass
class ExtractionMetadata:
    """Metadata about the extraction process and source."""
    source_path: Path
    source_type: str
    extraction_timestamp: datetime
    file_hash: str
    page_count: int
    extraction_status: str


class DataExtractor:
    def __init__(self):
        self.supported_types = {'.pdf', '.png', '.jpg', '.jpeg', '.tiff', '.bmp'}
        
    def _compute_file_hash(self, file_path: Path) -> str:
        """Compute SHA-256 hash of file for tracking."""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    
    def _get_source_type(self, file_path: Path) -> str:
        """Determine source type from file extension."""
        ext = file_path.suffix.lower()
        if ext == '.pdf':
            return 'pdf'
        elif ext in {'.png', '.jpg', '.jpeg', '.tiff', '.bmp'}:
            return 'image'
        raise ValueError(f"Unsupported file type: {ext}")
    
    def extract(self, file_path: str) -> pd.DataFrame:
        path = Path(file_path)
        source_type = self._get_source_type(path)
        file_hash = self._compute_file_hash(path)
        
        # Initialize metadata
        metadata = ExtractionMetadata(
            source_path=path,
            source_type=source_type,
            extraction_timestamp=datetime.now(),
            file_hash=file_hash,
            page_count=0,
            extraction_status='started'
        )
        
        extracted_data = []
        
        if source_type == 'image':
            # Process single image
            image = Image.open(path)
            text = pytesseract.image_to_string(image, lang='por')
            metadata.page_count = 1
            extracted_data.append({
                'raw_text': text,
                'page_number': 1,
                'metadata': metadata
            })
            
        else:  # PDF
            # Get page count
            with open(path, 'rb') as file:
                pdf = PdfReader(file)
                metadata.page_count = len(pdf.pages)
            
            # Convert and extract from each page
            images = convert_from_path(
                file_path,
                first_page=1,
                last_page=metadata.page_count
            )
            
            for i, image in enumerate(images, 1):
                text = pytesseract.image_to_string(image, lang='por')
                extracted_data.append({
                    'raw_text': text,
                    'page_number': i,
                    'metadata': metadata
                })
        
        # Create DataFrame with extraction results
        metadata.extraction_status = 'completed'
        df = pd.DataFrame(extracted_data)
        
        # Add extraction metadata as columns
        for field in metadata.__dataclass_fields__:
            df[f'meta_{field}'] = getattr(metadata, field)
        
        return df 