"""
Handles loading transformed data into the final CSV format.
"""

import pandas as pd
from typing import List
from .transformer import Transaction


class DataLoader:
    """
    Handles loading transformed data into the final CSV format.
    
    Responsible for converting Transaction objects into a CSV file
    that can be used for further analysis or reporting.
    """
    
    def load_to_csv(
        self, transactions: List[Transaction], output_path: str
    ) -> bool:
        """
        Saves transactions to a CSV file.
        
        Args:
            transactions: List of Transaction objects to save
            output_path: Path where the CSV file should be saved
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Convert to DataFrame
            df = pd.DataFrame([
                {
                    'date': t.date.strftime('%Y-%m-%d'),
                    'description': t.description,
                    'amount': str(t.amount)
                }
                for t in transactions
            ])
            
            # Save to CSV
            df.to_csv(output_path, index=False)
            return True
        except Exception as e:
            print(f"Error in loading stage: {e}")
            return False 