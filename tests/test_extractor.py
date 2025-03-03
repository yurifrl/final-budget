"""
Tests for the DataExtractor component using real files.
"""

from app.services import DataInput, DataExtractor


def test_extract_from_real_pdf():
    """
    Test extraction from real PDF files using DataInput to manage files.
    This test replicates how extraction works in the actual pipeline.
    """
    # Setup - use the same input directory as main
    data_input = DataInput("data/raw")
    extractor = DataExtractor()

    # Get the latest PDF file
    latest_file = data_input.latest
    print("--------------------------------")
    print(latest_file)
    print("--------------------------------")
    assert latest_file is not None, "No PDF files found in data/raw"
    
    # Extract text from the file
    text = extractor.extract(str(latest_file))
    assert text is not None, f"Failed to extract text from {latest_file}"
    assert len(text) > 0, "Extracted text is empty"
    print("--------------------------------")   
    print(text)
    print("--------------------------------")
    
    # Basic validation that we got bank statement text
    assert any(keyword in text.lower() for keyword in ["itau", "fatura", "extrato"]), \
        "Extracted text doesn't appear to be from an Itau bank statement" 