import os
from dataclasses import dataclass


@dataclass
class Config:
    llm_api_url: str
    llm_api_key: str
    llm_model: str

    @classmethod
    def from_env(cls) -> "Config":
        llm_url = os.environ.get("LLM_API_URL")
        llm_key = os.environ.get("LLM_API_KEY")
        llm_model = os.environ.get("LLM_MODEL")
        
        if not llm_url:
            raise ValueError("LLM_API_URL environment variable is required")
        if not llm_key:
            raise ValueError("LLM_API_KEY environment variable is required")
        if not llm_model:
            raise ValueError("LLM_MODEL environment variable is required")

        return cls(
            llm_api_url=llm_url,
            llm_api_key=llm_key,
            llm_model=llm_model
        ) 