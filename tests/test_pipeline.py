from app.services.data_input import DataInput


def test_extract_from_real_pdf():
    # Setup - use the correct data/raw/real path
    data_input = DataInput("data/raw/real")

    # Extract
    print("\n=== Sample Text ===")
    print(data_input.latest)  # First 500 chars
    print("\n=== End of Sample ===\n")