from typing import List
from .transformer import RawTransaction, EnrichedTransaction, PaymentChannel


class TransactionEnricher:
    def enrich(self, raw: RawTransaction) -> EnrichedTransaction:
        # Extract merchant details
        lines = raw.description.split('\n')
        merchant_name = lines[0].strip()
        merchant_location = lines[1].strip() if len(lines) > 1 else None
        
        # Detect payment channel
        desc_lower = raw.description.lower()
        channel = PaymentChannel.UNKNOWN
        if '*' in desc_lower:
            channel = PaymentChannel.WEB if '@' in desc_lower else PaymentChannel.MOBILE
        
        # Create enriched transaction
        return EnrichedTransaction(
            raw=raw,
            merchant_name=merchant_name,
            merchant_location=merchant_location,
            merchant_category=None,  # To be determined by another service
            payment_channel=channel,
            card_last_digits=None,  # To be determined by another service
            account_holder='YURI FREIRE LIMA'  # To be determined by another service
        )
    
    def enrich_many(self, transactions: List[RawTransaction]) -> List[EnrichedTransaction]:
        return [self.enrich(t) for t in transactions] 