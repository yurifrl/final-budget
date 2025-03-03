"""
Handles extraction of text from bank statement PDFs using OCR.
"""

import pytesseract
from typing import Optional
from pdf2image import convert_from_path


class DataExtractor:
    """
    Handles the extraction of raw text data from bank statement PDFs using OCR.
    
    This service is responsible for converting PDF bank statements
    into raw text that can be further processed by other components.
    """
    
    def extract(self, file_path: str) -> Optional[str]:
        """
        Extracts text content from a PDF file using OCR.
        
        Args:
            file_path: Path to the PDF file to process
            
        Returns:
            The extracted text if successful, None otherwise
        """
        try:
            # Convert first page of PDF to image
            images = convert_from_path(
                file_path, 
                first_page=1, 
                last_page=1
            )
            if not images:
                raise ValueError("No pages found in PDF")
            
            # Extract text using OCR
            text = pytesseract.image_to_string(images[0], lang='por')
            return text
        except Exception as e:
            print(f"Error in extraction stage: {e}")
            return None 