from app.data_input import DataInput
from app.pipeline import Pipeline
from app.config import Config

def test_pipeline_processes_real_pdf():
    """Test pipeline processing with real PDF data."""
    # Initialize pipeline with real data
    pipeline = Pipeline()
    data_input = DataInput("data/raw/real")
    
    # Process the latest file
    result = pipeline.process_file(data_input.latest)
    
    # Print result for inspection
    print("\n=== Processed Result ===")
    print(result)
    print("\n=== End of Result ===\n")