import os
from dataclasses import dataclass


@dataclass
class Config:
    llm_api_url: str
    llm_model: str = "deepseek-r1:1.5b"

    @classmethod
    def from_env(cls) -> "Config":
        llm_url = os.environ.get("LLM_API_URL")
        if not llm_url:
            raise ValueError("LLM_API_URL environment variable is required")
            
        return cls(llm_api_url=llm_url) 