import pandas as pd
from datetime import datetime


class DataTransformer:
    """
    Enriches transaction data with derived fields and analytics.
    """
    
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        required_cols = {'date', 'amount', 'description', 'merchant_name'}
        missing = required_cols - set(df.columns)
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
            
        # Convert types
        result = df.copy()
        result['date'] = pd.to_datetime(result['date'])
        result['amount'] = pd.to_numeric(
            result['amount'].str.replace(',', '.')
        )
        
        # Add derived fields
        result['transform_timestamp'] = datetime.now()
        result['is_debit'] = result['amount'] < 0
        result['abs_amount'] = result['amount'].abs()
        result['month'] = result['date'].dt.month
        result['year'] = result['date'].dt.year
        result['day_of_week'] = result['date'].dt.day_name()
        
        # Clean merchant info
        result['merchant_name'] = result['merchant_name'].fillna('Unknown')
        result['merchant_location'] = (
            result['merchant_location'].fillna('Unknown')
        )
        
        # Add summary stats as metadata
        debits = result[result['amount'] < 0]['amount'].sum()
        credits = result[result['amount'] > 0]['amount'].sum()
        
        stats = {
            'total_transactions': len(result),
            'date_min': result['date'].min(),
            'date_max': result['date'].max(),
            'total_credits': credits,
            'total_debits': debits,
            'unique_merchants': result['merchant_name'].nunique()
        }
        
        # Add stats as columns for lineage
        for key, value in stats.items():
            result[f'meta_{key}'] = value
            
        return result 