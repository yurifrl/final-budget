from .data_input import DataInput
from ..config import Config
from pathlib import Path
from typing import Dict, Any
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
import json


class Pipeline:
    def __init__(self, config: Config):
        self.config = config
        self.embeddings = OllamaEmbeddings(
            base_url=config.llm_api_url,
            model=config.llm_model,
            api_key=config.llm_api_key
        )
        self.llm = Ollama(
            base_url=config.llm_api_url,
            model=config.llm_model,
            api_key=config.llm_api_key
        )

        # Initialize text splitter for chunking documents
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )

    def process_file(self, file_path: Path) -> Dict[str, Any]:
        # Load and process the PDF
        loader = PyPDFLoader(str(file_path))
        pages = loader.load()

        # Split the document into chunks
        chunks = self.text_splitter.split_documents(pages)

        # Create a vector store from the chunks
        vectorstore = FAISS.from_documents(chunks, self.embeddings)

        # Create a retrieval chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever()
        )

        # Define the query to extract structured data
        query = """
        Extract the following information from this document in JSON format:
        - Date
        - Amount
        - Description
        - Category
        - Type (income/expense)

        Format the response as a valid JSON object.
        """

        # Get the response
        response = qa_chain.invoke({"query": query})

        # Parse the response into a dictionary
        try:
            result = json.loads(response["result"])
        except json.JSONDecodeError:
            # If JSON parsing fails, return a structured error
            result = {
                "error": "Failed to parse LLM response as JSON",
                "raw_response": response["result"]
            }

        # Create output path
        output_dir = Path("data/processed")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"{file_path.stem}_processed.json"

        # Save the results
        with open(output_path, "w") as f:
            json.dump(result, f, indent=2)

        return result


    def run(self) -> bool:
        input = DataInput("data/raw/real")

        success = True
        for file_path in input.files:
            try:
                output_path = self.process_file(file_path)
                print(f"Successfully processed {file_path} -> {output_path}")
            except Exception as e:
                print(f"Failed to process {file_path}: {e}")
                success = False
        return success
