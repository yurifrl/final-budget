from .config import Config
from .data_input import DataInput
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from .models import Models
from pathlib import Path
from typing import Any
from uuid import uuid4

class Ingester:
    def __init__(self, config: Config):
        self.config = config

        # Initialize the models
        self.models = Models(config)
        self.embeddings = self.models.embeddings_ollama
        self.llm = self.models.llm_ollama

        # Initialize vector store with Chroma from langchain-chroma
        self.vector_store = Chroma(
            collection_name="documents",
            embedding_function=self.embeddings,
            persist_directory=self.config.db_folder
        )

        # Initialize text splitter with configurable parameters for flexibility in document processing
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=50,
            separators=["\n", " "]
        )


    def ingest_file(self, file_path: Path) -> Any:
        # Load and split document into manageable chunks for vector storage
        loader = PyPDFLoader(str(file_path))
        loaded_documents = loader.load()
        
        # Split documents into chunks with overlap to maintain context across chunks
        documents = self.text_splitter.split_documents(loaded_documents)
        
        # Generate unique IDs for each document chunk for retrieval
        uuids = [str(uuid4()) for _ in range(len(documents))]
        
        # Store documents in vector store for later retrieval and querying
        self.vector_store.add_documents(documents=documents, ids=uuids)
        
        return {"processed_chunks": len(documents), "file": str(file_path)}

    def run(self, input: DataInput) -> Any:
        for file_path in input.files:
            output = self.process_file(file_path)
            print(output)

        return None