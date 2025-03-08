from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from app.models import Models
from app.config import Config
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class Transaction(BaseModel):
    """Represents a single bank transaction entry."""

    date: str = Field(
        description="The date when the transaction occurred in YYYY-MM-DD format"
    )
    description: str = Field(description="The description or type of the transaction")
    value: float = Field(
        description="The transaction amount (negative for debits, positive for credits)"
    )
    balance: Optional[float] = Field(
        default=None, description="The account balance after this transaction"
    )


class TransactionResponse(BaseModel):
    """Response format for transaction queries."""

    transactions: List[Transaction] = Field(description="List of matching transactions")


class Chat:
    def __init__(self, config: Config):
        # Initialize the models
        models = Models(config)
        self.embeddings = models.get_embeddings()
        self.llm = models.get_llm().with_structured_output(TransactionResponse)

        # Initialize the vector store
        self.vector_store = Chroma(
            collection_name="transactions",
            embedding_function=self.embeddings,
            persist_directory=config.db_folder,
        )

    def retrieve(self, query: str) -> TransactionResponse:
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are a financial assistant specialized in analyzing bank transactions.
                         You must return a valid JSON object with this exact structure:
                         {
                           "transactions": [
                             {
                               "date": "YYYY-MM-DD",
                               "description": "transaction description",
                               "value": 123.45,
                               "balance": 1234.56
                             }
                           ]
                         }
                         
                         Important:
                         - dates must be in YYYY-MM-DD format
                         - values must be numbers (not strings)
                         - balance can be null
                         - description must be a string
                         - do not include any additional text or explanation""",
                ),
                (
                    "human",
                    "Find transactions matching this query: {input}\nBank statement data: {context}",
                ),
            ]
        )

        retriever = self.vector_store.as_retriever(kwargs={"k": 10})
        combine_docs_chain = create_stuff_documents_chain(self.llm, prompt)
        retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)

        result = retrieval_chain.invoke({"input": query})
        print(result)
        return result
        # return TransactionResponse.model_validate_json(result["answer"])
