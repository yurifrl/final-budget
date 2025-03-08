from app.data_input import DataInput
from app.ingest import Ingester
from app.config import Config
from app.chat import Chat
def test_ingest():
    """Test pipeline processing with real PDF data."""
    # Initialize pipeline with real data
    ingester = Ingester(Config.from_env())
    data_input = DataInput("data/raw/real")
    
    # Process the latest file
    result = ingester.ingest_file(data_input.latest)
    
    # Print result for inspection
    print("\n=== Processed Result ===")
    print(result)
    print("\n=== End of Result ===\n")

def test_chat():
    """Test chat pipeline with real data."""
    # Initialize pipeline with real data
    chat = Chat(Config.from_env())
    result = chat.retrieve("Show me all transactions from February 1st to February 28th")
    print(result)
