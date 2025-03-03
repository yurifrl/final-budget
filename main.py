"""
Main entry point for the bank statement processing pipeline.
"""

import sys
from pathlib import Path
from app.services.all import Pipeline


def main(
    input_directory: str = "data/raw",
    output_path: str = "data/processed/transactions.csv"
) -> int:
    """
    Run the bank statement processing pipeline.
    
    Args:
        input_directory: Directory containing bank statement files
        output_path: Path where to save the processed transactions
    
    Returns:
        int: 0 for success, 1 for failure
    """
    # Validate input directory exists
    if not Path(input_directory).is_dir():
        print(f"Error: Input directory '{input_directory}' does not exist")
        return 1

    # Create output directory if it doesn't exist
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    # Run pipeline
    pipeline = Pipeline(input_directory)
    success = pipeline.run(output_path)
    
    if not success:
        print("Pipeline failed. Check the logs for details.")
        return 1
    
    return 0


if __name__ == "__main__":
    # Use command line arguments if provided, otherwise use defaults
    input_dir = sys.argv[1] if len(sys.argv) > 1 else "data/raw"
    output_file = sys.argv[2] if len(sys.argv) > 2 else "data/processed/transactions.csv"
    
    sys.exit(main(input_dir, output_file))
