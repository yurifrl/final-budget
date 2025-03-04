from app.services.parser import LLMDataFetchParser, JSONExtractParser
from app.config import Config
import pandas as pd


def test_parser_output():
    config = Config.from_env()
    llmfetcher = LLMDataFetchParser(config.llm_api_url, config.llm_model)
    json_parser = JSONExtractParser()

    input_df = pd.DataFrame({
        'raw_text': ['Statement date: 2024-01-15\nMcDonalds SP R$ 50,00'],
        'page_number': [1],
        'meta_file_hash': ['abc123']
    })

    llm_result = llmfetcher.parse(input_df)
    json_result = json_parser.parse(llm_result)

    print("\n=== Parsed JSON Result ===")
    print(json_result.iloc[0])
    print("=== End of JSON Result ===\n") 