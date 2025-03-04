from app.services.data_input import DataInput
from pathlib import Path
import json
from app.services.pipeline import Pipeline
from app.config import Config
import os


def test_pipeline_processes_real_pdf():
    """Test pipeline processing with real PDF data."""
    # Initialize pipeline with real data
    pipeline = Pipeline(Config.from_env())
    
    # Get the latest file
    data_input = DataInput("data/raw/real")
    latest_file = data_input.latest
    
    # Process the latest file
    result = pipeline.process_file(latest_file)
    
    # Print result for inspection
    print("\n=== Processed Result ===")
    print(result)
    print("\n=== End of Result ===\n")