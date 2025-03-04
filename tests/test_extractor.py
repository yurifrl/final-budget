from app.services.data_input import DataInput
from app.services.extractor import DataExtractor
import pandas as pd
from pathlib import Path


def test_extract_from_real_pdf():
    # Setup - use the correct data/raw/real path
    data_input = DataInput("data/raw/real")
    extractor = DataExtractor()

    # Get the latest file
    file = data_input.latest
    
    # Extract text and metadata
    df = extractor.extract(str(file))
  
    print("\n=== Sample Text ===")
    print(df['raw_text'].iloc[0])  # First 500 chars
    print("\n=== End of Sample ===\n")