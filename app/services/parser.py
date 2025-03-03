"""
Handles AI-based parsing of raw text into structured transaction data.
"""

import json
import requests
from typing import List, Dict, Any


class AIParser:
    """
    Handles the AI-based parsing of raw text into structured transaction data.
    
    Uses a local LLM to convert unstructured bank statement text into a
    structured format that can be processed by the transformer.
    """
    
    def __init__(self, model: str = "llama2"):
        self.model = model
    
    def parse(self, raw_text: str) -> List[Dict[str, Any]]:
        """
        Parses raw text into structured transaction data using AI.
        
        Args:
            raw_text: The raw text extracted from the bank statement
            
        Returns:
            List of dictionaries containing structured transaction data
        """
        try:
            prompt = (
                "Parse this bank statement text into a JSON array of transactions.\n"
                "Each transaction should have:\n"
                "- date (YYYY-MM-DD)\n"
                "- description (full original text)\n"
                "- amount (string with 2 decimal places, negative for debits)\n"
                "- merchant_name (name of establishment)\n"
                "- merchant_location (city/location if available)\n"
                "- category (transaction category if available)\n"
                "- payment_method (web/mobile/pos/atm based on * or @ symbols)\n"
                "- card_last_digits (if available)\n"
                "\nOnly return the JSON array, no other text.\n"
                f"Text to parse:\n{raw_text}"
            )
            
            response = requests.post(
                'http://localhost:11434/api/generate',
                json={"model": self.model, "prompt": prompt}
            )
            
            return json.loads(response.json().get('response', '[]'))
        except Exception as e:
            print(f"Error in parsing stage: {e}")
            return [] 