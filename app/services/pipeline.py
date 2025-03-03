"""
Orchestrates the ETL pipeline for processing bank statements.
"""

from .data_input import DataInput
from .extractor import DataExtractor, ExtractedData
from .parser import AIParser
from .transformer import DataTransformer
from .loader import DataLoader
from typing import Optional, List
from pathlib import Path


class Pipeline:
    """
    Orchestrates the complete ETL pipeline.
    
    Coordinates the flow of data through each stage of processing:
    input → extraction → parsing → transformation → loading.
    """
    
    def __init__(self):
        self.input = DataInput("data/raw/real")
        self.extractor = DataExtractor()
        self.parser = AIParser()
        self.transformer = DataTransformer()
        self.loader = DataLoader()
    
    def process_file(self, file_path: Path) -> bool:
        """Process a single file through the pipeline."""
        try:
            print(f"\nProcessing file: {file_path}")
            
            # Extract text and metadata
            print("Extracting text...")
            extracted_data = self.extractor.extract(str(file_path))
            if not extracted_data:
                print(f"Failed to extract text from {file_path}")
                return False
                
            # Parse the extracted text
            print("Parsing data...")
            parsed_data = self.parser.parse(extracted_data.raw_text)
            if not parsed_data:
                print(f"Failed to parse data from {file_path}")
                return False

            # Transform data into transactions
            print("Transforming data...")
            raw_transactions = self.transformer.transform(
                parsed_data,
                str(extracted_data.file_path),
                extracted_data.file_type
            )
            if not raw_transactions:
                print(f"Failed to transform data from {file_path}")
                return False

            # Load transactions to CSV
            print("Loading to CSV...")
            if not self.loader.load_to_csv(raw_transactions):
                print(f"Failed to load data from {file_path}")
                return False

            print(f"Successfully processed {file_path}")
            return True

        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return False

    def run(self) -> bool:
        """Run the pipeline on all files in the input directory."""
        success = True
        for file_path in self.input.files:
            if not self.process_file(file_path):
                success = False
        return success 