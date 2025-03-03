import pytesseract
from typing import Optional
from pdf2image import convert_from_path
from pypdf import PdfReader
from pathlib import Path
from PIL import Image
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ExtractedData:
    """Container for extracted text data and its metadata."""
    raw_text: str
    file_path: Path
    file_type: str  # 'pdf' or 'image'
    page_count: int
    extraction_date: datetime
    file_name: str
    file_size: int  # in bytes
    
    @property
    def is_multipage(self) -> bool:
        return self.page_count > 1


class DataExtractor:
    # Supported image formats
    IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.tiff', '.bmp'}
    
    def is_image_file(self, file_path: str) -> bool:
        """Check if the file is a supported image format."""
        return Path(file_path).suffix.lower() in self.IMAGE_EXTENSIONS
    
    def is_pdf_file(self, file_path: str) -> bool:
        """Check if the file is a PDF."""
        return Path(file_path).suffix.lower() == '.pdf'
    
    def get_page_count(self, file_path: str) -> int:
        """Get the number of pages in a PDF file."""
        if not self.is_pdf_file(file_path):
            return 1  # Image files are single page
            
        with open(file_path, 'rb') as file:
            pdf = PdfReader(file)
            return len(pdf.pages)
    
    def extract(self, file_path: str) -> Optional[ExtractedData]:
        """Extract text from a file and return it with metadata."""
        try:
            path = Path(file_path)
            file_size = path.stat().st_size
            
            if self.is_image_file(file_path):
                # Handle image files directly
                print(f"Processing image file: {file_path}")
                image = Image.open(file_path)
                text = pytesseract.image_to_string(image, lang='por')
                
                return ExtractedData(
                    raw_text=text,
                    file_path=path,
                    file_type='image',
                    page_count=1,
                    extraction_date=datetime.now(),
                    file_name=path.name,
                    file_size=file_size
                )
            
            elif self.is_pdf_file(file_path):
                # Handle PDF files
                print(f"Processing PDF file: {file_path}")
                total_pages = self.get_page_count(file_path)
                print(f"PDF has {total_pages} pages")
                
                # Convert all pages to images
                images = convert_from_path(
                    file_path,
                    first_page=1,
                    last_page=total_pages
                )
                if not images:
                    raise ValueError("No pages found in PDF")
                
                # Extract text from all pages
                texts = []
                for i, image in enumerate(images, 1):
                    print(f"Processing page {i}/{total_pages}")
                    text = pytesseract.image_to_string(image, lang='por')
                    texts.append(text)
                
                # Combine all texts with page separators
                full_text = "\n=== Page Break ===\n".join(texts)
                
                return ExtractedData(
                    raw_text=full_text,
                    file_path=path,
                    file_type='pdf',
                    page_count=total_pages,
                    extraction_date=datetime.now(),
                    file_name=path.name,
                    file_size=file_size
                )
            
            else:
                suffix = Path(file_path).suffix
                raise ValueError(f"Unsupported file format: {suffix}")
                
        except Exception as e:
            print(f"Error in extraction stage: {e}")
            return None 