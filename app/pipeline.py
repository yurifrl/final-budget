from .data_input import DataInput
from .config import Config
from pathlib import Path
from typing import Any
import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chains import create_retrieval_chain, create_stuff_documents_chain
from uuid import uuid4

class Pipeline:
    def __init__(self, config: Config):
        self.config = config

        self.llm = ChatOpenAI(
           model="gpt-4-vision-preview",
           api_key=config.llm_api_key,
           base_url=config.llm_api_url,
           temperature=0.6
       )
        self.embeddings = OpenAIEmbeddings(
            model=config.embedding_model_name
        )
        # # Use Ollama for local model inference
        # self.llm = ChatOllama(
        #     model=config.model_name,
        #     temperature=config.temperature
        # )
        # self.embeddings = OllamaEmbeddings(
        #     model=config.embedding_model_name
        # )
    
        # Initialize text splitter with configurable parameters for flexibility in document processing
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=50,
            separators=["\n", " "]
        )
        
        # Initialize vector store with persistent storage for document embeddings
        self.vector_store = Chroma(
            collection_name="documents",
            embedding_function=self.embeddings,
            persist_directory="./db/chroma_langchain_db"
        )
        
        # Set up retrieval chain for semantic search with top-k results
        self.retriever = self.vector_store.as_retriever(kwargs={"k": 4})
        
        # Create document processing chain for combining retrieved documents
        self.combine_docs_chain = create_stuff_documents_chain(
            self.llm, 
            config.prompt
        )
        
        # Create final retrieval chain that combines search and processing
        self.retrieval_chain = create_retrieval_chain(
            self.retriever,
            self.combine_docs_chain
        )

    def process_file(self, file_path: Path) -> Any:
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
        
        # Process query using the retrieval chain
        if input.query:
            result = self.retrieval_chain.invoke({"input": input.query})
            return result.get("answer")
        return None