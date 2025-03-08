import os
from dataclasses import dataclass


@dataclass
class Config:
    openai_api_url: str
    openai_api_key: str
    ollama_host: str
    data_folder: str
    db_folder: str

    @classmethod
    def from_env(cls) -> "Config":
        openai_api_url = os.environ.get("OPENAI_API_URL")
        openai_api_key = os.environ.get("OPENAI_API_KEY")
        ollama_host = os.environ.get("OLLAMA_HOST")
        data_folder = "./data/raw/real"
        db_folder = "./db/chroma_langchain_db"

        if not openai_api_url:
            raise ValueError("OPENAI_API_URL environment variable is required")
        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        if not ollama_host:
            raise ValueError("OLLAMA_HOST environment variable is required")
 
        return cls(
            openai_api_url=openai_api_url,
            openai_api_key=openai_api_key,
            ollama_host=ollama_host,
            data_folder=data_folder,
            db_folder=db_folder
        ) 