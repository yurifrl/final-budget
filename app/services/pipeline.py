"""
Orchestrates the ETL pipeline for processing bank statements.
"""

from .extractor import DataExtractor
from .parser import AIParser
from .transformer import DataTransformer
from .loader import DataLoader
from .data_input import DataInput


class Pipeline:
    """
    Orchestrates the complete ETL pipeline.
    
    Coordinates the flow of data through each stage of processing:
    input → extraction → parsing → transformation → loading.
    """
    
    def __init__(self, input_directory: str = "data/raw"):
        self.input = DataInput(input_directory)
        self.extractor = DataExtractor()
        self.parser = AIParser()
        self.transformer = DataTransformer()
        self.loader = DataLoader()
    
    def run(self, output_path: str) -> bool:
        """
        Runs the complete ETL pipeline on all input files.
        
        Args:
            output_path: Path where the CSV should be saved
            
        Returns:
            True if successful, False otherwise
        """
        print("Starting pipeline...")
        
        # Process each input file
        for file_path in self.input:
            print(f"Processing file: {file_path}")
            
            # Extract
            print("Extracting text from image...")
            raw_text = self.extractor.extract(str(file_path))
            if not raw_text:
                continue
                
            # Parse with AI
            print("Parsing text with AI...")
            parsed_data = self.parser.parse(raw_text)
            if not parsed_data:
                continue
                
            # Transform
            print("Transforming data...")
            transactions = self.transformer.transform(parsed_data)
            if not transactions:
                continue
                
            # Load
            print("Loading data to CSV...")
            success = self.loader.load_to_csv(transactions, output_path)
            
            if not success:
                print(f"Failed to process file: {file_path}")
                continue
                
        print(f"Pipeline completed. Output: {output_path}")
        return True 