from .data_input import DataInput
from .extractor import DataExtractor
from .parser import LLMDataFetchParser, JSONExtractParser
from .transformer import DataTransformer
from .loader import DataLoader
from ..config import Config
from pathlib import Path
from typing import Dict, Any, List


class Pipeline:    
    def __init__(self, config: Config, input_dir: str = "data/raw/real"):
        self.input = DataInput(input_dir)
        self.extractor = DataExtractor()
        # Initialize the parsers
        self.llm_fetch_parser = LLMDataFetchParser(config.llm_api_url, config.llm_model)
        self.json_extract_parser = JSONExtractParser()
        self.transformer = DataTransformer()
        self.loader = DataLoader()
    
    def process_file(self, file_path: Path) -> Dict[str, Any]:
        # Extract - Convert raw file to DataFrame with text and metadata
        df = self.extractor.extract(str(file_path))
        
        # Parse - Chain the parsers
        df = self.llm_fetch_parser.parse(df)  # First: Fetch data from LLM API
        df = self.json_extract_parser.parse(df)  # Second: Extract JSON data
        
        # Transform - Add derived fields and analytics
        df = self.transformer.transform(df)
        
        # Load - Save final state to CSV
        output_path = self.loader.load_to_csv(df)
        
        return output_path

    def run(self) -> bool:
        success = True
        for file_path in self.input.files:
            try:
                output_path = self.process_file(file_path)
                print(f"Successfully processed {file_path} -> {output_path}")
            except Exception as e:
                print(f"Failed to process {file_path}: {e}")
                success = False
        return success 