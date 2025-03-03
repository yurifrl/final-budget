"""
Handles transformation of parsed data into domain objects.
"""

from typing import List, Dict, Any
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class Transaction:
    """Data model for a bank transaction."""
    date: datetime
    description: str
    amount: Decimal
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Transaction':
        """
        Creates a Transaction instance from a dictionary.
        
        Args:
            data: Dictionary containing transaction data
            
        Returns:
            A new Transaction instance
        """
        return cls(
            date=datetime.strptime(data['date'], '%Y-%m-%d'),
            description=data['description'],
            amount=Decimal(str(data['amount']))
        )


class DataTransformer:
    """
    Handles transformation of parsed data into domain objects.
    
    Converts the raw parsed data into strongly-typed Transaction objects
    that can be used by the rest of the application.
    """
    
    def transform(self, transactions: List[Dict[str, Any]]) -> List[Transaction]:
        """
        Transforms raw transaction data into Transaction objects.
        
        Args:
            transactions: List of dictionaries containing transaction data
            
        Returns:
            List of Transaction objects
        """
        try:
            return [Transaction.from_dict(t) for t in transactions]
        except Exception as e:
            print(f"Error in transformation stage: {e}")
            return [] 