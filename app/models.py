from .config import Config
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_ollama import ChatOllama, OllamaEmbeddings

class Models:
    def __init__(self, config: Config):
        self.config = config

        # OpenAI
        self.llm_openai = ChatOpenAI(
            api_key=config.openai_api_key,
            base_url=config.openai_api_url,
            model="gpt-4-vision-preview",
            temperature=0.6,
        )
        self.embeddings_openai = OpenAIEmbeddings(
            model="text-embedding-3-large"
        )

        # Ollama
        self.llm_ollama = ChatOllama(
            base_url=config.ollama_host,
            model="llama3.1:8b",
            temperature=0
        )
        self.embeddings_ollama = OllamaEmbeddings(
            base_url=config.ollama_host,
            model="mxbai-embed-large"
        )