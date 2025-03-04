from .data_input import DataInput
from ..config import Config
from pathlib import Path
from typing import Dict, Any


class Pipeline:
    def __init__(self, config: Config, input_dir: str = "data/raw/real"):
        self.input = DataInput(input_dir)

    def process_file(self, file_path: Path) -> Dict[str, Any]:
        # ????
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