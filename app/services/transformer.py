"""
Handles transformation of parsed data into domain objects.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum
from .data_input import FileType


class PaymentChannel(Enum):
    MOBILE = "mobile"
    WEB = "web"
    POS = "pos"  # Point of sale
    ATM = "atm"
    UNKNOWN = "unknown"


@dataclass
class RawTransaction:
    date: datetime
    description: str
    amount: Decimal
    source_file: str
    source_type: FileType

    @classmethod
    def from_dict(
        cls, 
        data: Dict[str, Any],
        source_file: str,
        source_type: FileType
    ) -> 'RawTransaction':
        return cls(
            date=datetime.strptime(data['date'], '%Y-%m-%d'),
            description=data['description'],
            amount=Decimal(str(data['amount'])),
            source_file=source_file,
            source_type=source_type
        )


@dataclass
class EnrichedTransaction:
    raw: RawTransaction
    merchant_name: str
    merchant_location: Optional[str]
    merchant_category: Optional[str]
    payment_channel: PaymentChannel
    card_last_digits: Optional[str]
    account_holder: str


class DataTransformer:
    """
    Handles transformation of parsed data into domain objects.
    
    Converts the raw parsed data into strongly-typed Transaction objects
    that can be used by the rest of the application.
    """
    
    def transform(
        self,
        transactions: List[Dict[str, Any]],
        source_file: str,
        source_type: FileType
    ) -> List[RawTransaction]:
        """
        Transforms raw transaction data into Transaction objects.
        
        Args:
            transactions: List of dictionaries containing transaction data
            source_file: The file from which the transaction data was read
            source_type: The type of file from which the transaction data was read
            
        Returns:
            List of Transaction objects
        """
        try:
            return [
                RawTransaction.from_dict(t, source_file, source_type)
                for t in transactions
            ]
        except Exception as e:
            print(f"Error in transformation stage: {e}")
            return [] 