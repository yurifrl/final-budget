import json
import re
import requests
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime
from dataclasses import dataclass
from uuid import uuid4
from abc import ABC, abstractmethod


@dataclass
class TransformationMetadata:
    """Metadata about the transformation process."""
    transformation_id: str
    source_hash: str  # Links to extraction metadata
    transformation_timestamp: datetime
    model_version: str
    schema_version: str
    validation_status: str
    row_count: int = 0
    error_count: int = 0


class BaseParser(ABC):
    """Base class for all parsers in the pipeline."""
    
    @abstractmethod
    def parse(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process the DataFrame and return the enriched version."""
        pass


class LLMDataFetchParser(BaseParser):
    """Handles the LLM API interaction to fetch data."""
    
    def __init__(self, api_url: str, model: str):
        self.api_url = api_url
        self.model = model
    
    def parse(self, df: pd.DataFrame) -> pd.DataFrame:
        # Add raw API responses to DataFrame
        df['raw_api_response'] = df['raw_text'].apply(self._fetch_from_api)
        return df
    
    def _fetch_from_api(self, text: str) -> str:
        """Fetch response from LLM API."""
        prompt = (
            "Parse this bank statement text into a JSON array of "
            "transactions.\nEach transaction should have:\n"
            "- date (YYYY-MM-DD)\n"
            "- description (full original text)\n"
            "- amount (string with 2 decimal places)\n"
            "- merchant_name (name of establishment)\n"
            "- merchant_location (city/location if available)\n"
            "\nOnly return the JSON array, no other text.\n"
            f"Text to parse:\n{text}"
        )
        
        response = requests.post(
            f"{self.api_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": True
            }
        )
        
        # Collect the full response
        full_response = ""
        for line in response.iter_lines():
            if line:
                chunk = json.loads(line.decode('utf-8'))
                if chunk.get('response'):
                    full_response += chunk['response']

        return full_response


class JSONExtractParser(BaseParser):
    """Extracts structured JSON data from API responses."""
    
    def __init__(self):
        self.schema_version = "1.0.0"
    
    def parse(self, df: pd.DataFrame) -> pd.DataFrame:
        all_transactions: List[Dict[str, Any]] = []
        transform_id = str(uuid4())
        
        # Process each API response
        for _, row in df.iterrows():
            # Extract JSON array from markdown response
            json_match = re.search(
                r'```json\s*(\[.*?\])\s*```',
                row['raw_api_response'],
                re.DOTALL
            )
            if not json_match:
                raise ValueError("No JSON array found in API response")
            
            # Parse the JSON array
            transactions = json.loads(json_match.group(1))
            
            # Add metadata to each transaction
            for t in transactions:
                t.update({
                    'page_number': row['page_number'],
                    'parse_timestamp': datetime.now(),
                    'transform_id': transform_id,
                    'schema_version': self.schema_version
                })
                all_transactions.append(t)
        
        if not all_transactions:
            raise ValueError("No valid transactions found in input")
            
        # Create DataFrame with parsed results
        parsed_df = pd.DataFrame(all_transactions)
        
        # Merge with original DataFrame to maintain lineage
        return df.merge(parsed_df, on='page_number', how='right') 