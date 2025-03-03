from app.services.data_input import DataInput
from app.services.extractor import DataExtractor, ExtractedData
from pathlib import Path


def test_extract_from_real_pdf():
    # Setup - use the correct data/raw/real path
    data_input = DataInput("data/raw/real")
    extractor = DataExtractor()

    # Get the latest file
    file = data_input.latest
    assert file is not None, "No files found in data/raw/real"
    
    # Extract text and metadata
    print("\nExtracting text and metadata...")
    extracted_data = extractor.extract(str(file))
    assert extracted_data is not None, f"Failed to extract data from {file}"
    
    # Verify metadata
    assert isinstance(extracted_data, ExtractedData)
    assert extracted_data.file_path == Path(file)
    assert extracted_data.file_type in ['pdf', 'image']
    assert extracted_data.page_count > 0
    assert len(extracted_data.raw_text) > 0
    assert extracted_data.file_size > 0
    
    # Print extracted information
    print("\n=== Extracted Data ===")
    print(f"File: {extracted_data.file_name}")
    print(f"Type: {extracted_data.file_type}")
    print(f"Pages: {extracted_data.page_count}")
    print(f"Size: {extracted_data.file_size:,} bytes")
    print(f"Date: {extracted_data.extraction_date}")
    print("\n=== Extracted Text ===")
    print(extracted_data.raw_text)
    print("\n=== End of Text ===\n")
