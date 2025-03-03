"""
Handles loading transformed data into the final CSV format.
"""

import pandas as pd
from typing import List, Union
from .transformer import RawTransaction, EnrichedTransaction


class DataLoader:
    """
    Handles loading transformed data into the final CSV format.
    
    Responsible for converting Transaction objects into a CSV file
    that can be used for further analysis or reporting.
    """
    
    def load_to_csv(
        self,
        transactions: List[Union[RawTransaction, EnrichedTransaction]],
        output_path: str
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
            records = []
            for t in transactions:
                if isinstance(t, RawTransaction):
                    records.append({
                        'date': t.date.strftime('%Y-%m-%d'),
                        'description': t.description,
                        'amount': str(t.amount),
                        'source_file': t.source_file,
                        'source_type': t.source_type.value
                    })
                else:  # EnrichedTransaction
                    records.append({
                        'date': t.raw.date.strftime('%Y-%m-%d'),
                        'description': t.raw.description,
                        'amount': str(t.raw.amount),
                        'merchant_name': t.merchant_name,
                        'merchant_location': t.merchant_location or '',
                        'merchant_category': t.merchant_category or '',
                        'payment_channel': t.payment_channel.value,
                        'card_last_digits': t.card_last_digits or '',
                        'account_holder': t.account_holder,
                        'source_file': t.raw.source_file,
                        'source_type': t.raw.source_type.value
                    })
            
            df = pd.DataFrame(records)
            df.to_csv(output_path, index=False)
            return True
        except Exception as e:
            print(f"Error in loading stage: {e}")
            return False 