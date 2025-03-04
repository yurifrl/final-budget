"""
Data loading layer for bank statement processing.

This layer handles:
1. Saving processed data to CSV format
2. Data versioning and organization
"""

import pandas as pd
from pathlib import Path


class DataLoader:
    def __init__(self, output_dir: str = "data/processed"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def load_to_csv(self, df: pd.DataFrame) -> Path:
        if df.empty:
            raise ValueError("No data to save")
        
        # Save transaction data
        output_path = self.output_dir / "transactions.csv"
        df.to_csv(output_path, index=False)
        
        return output_path 