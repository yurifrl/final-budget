import sys
from app.data_input import DataInput
from app.pipeline import Pipeline
from app.config import Config

def main() -> int:
    # Run pipeline
    config = Config.from_env()
    pipeline = Pipeline(config)
    input = DataInput("data/raw/real")

    success = pipeline.run(input)

    if not success:
        print("Pipeline failed. Check the logs for details.")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
