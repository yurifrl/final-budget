from app.data_input import DataInput
from app.config import Config
from app.foo import Foo

def test_ingest():
    """Test pipeline processing with real PDF data."""
    # Initialize pipeline with real data
    ingester = Foo(Config.from_env())
    data_input = DataInput("data/raw/real")
    
    # Process the latest file
    result = ingester.ingest_file(data_input.latest)
    
    # Print result for inspection
    print("\n=== Processed Result ===")
    print(result)
    print("\n=== End of Result ===\n")
