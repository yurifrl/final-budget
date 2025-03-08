from app.config import Config
from app.data_input import DataInput
from app.models import Models
from datetime import datetime
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from pathlib import Path
from pydantic import BaseModel, Field
from typing import Any
from typing import Optional, List
from uuid import uuid4
from pdf2image import convert_from_path
import os
import base64
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser

import io
import json

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


class Foo:
    def __init__(self, config: Config):
        self.models = Models(config)
        self.embeddings = self.models.get_embeddings()
        self.llm = self.models.get_llm().with_structured_output(TransactionResponse)
        self.vision_model = ChatOpenAI(
            temperature=0.5, 
            model="gpt-4o", 
            # max_tokens=1024
        ).with_structured_output(TransactionResponse)
        self.verify_model = ChatOpenAI(
            temperature=0.0,
            model="gpt-4o",
        )

    def ingest_file(self, file_path):
        # Convert PDF directly to images in memory
        images = convert_from_path(file_path)
        
        # Convert all images to base64
        image_contents = []
        for page_num, image in enumerate(images, 1):
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            image_base64 = base64.b64encode(img_byte_arr).decode('utf-8')
            image_contents.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}})
            
        vision_prompt = """
        Given these bank statement images, extract all transactions you can find from all pages.
        For each transaction provide:
        - The transaction date in YYYY-MM-DD format
        - The transaction description exactly as shown
        - The transaction value (negative for debits, positive for credits)
        - The account balance after this transaction if available (can be null if not shown)

        Return the transactions in chronological order.
        Make sure to format the response as a list of transactions with all required fields.
        Each transaction must have: date, description, value, and balance (which can be null).
        """
        
        message = HumanMessage(
            content=[
                {"type": "text", "text": vision_prompt},
                *image_contents
            ]
        )

        result = self.vision_model.invoke([message])
        
        # Save result as JSON with same name as input file
        output_dir = Path("data/processed")
        output_dir.mkdir(parents=True, exist_ok=True)
        input_filename = Path(file_path).stem
        output_file = output_dir / f"{input_filename}.json"
        
        with open(output_file, "w") as f:
            json.dump(result.model_dump(), f, indent=2)
        
        # Print token usage
        if hasattr(result, 'llm_output') and result.llm_output:
            token_usage = result.llm_output.get('token_usage', {})
            print(f"\nToken Usage:")
            print(f"Prompt tokens: {token_usage.get('prompt_tokens', 'N/A')}")
            print(f"Completion tokens: {token_usage.get('completion_tokens', 'N/A')}")
            print(f"Total tokens: {token_usage.get('total_tokens', 'N/A')}")
        
        # Verify the extracted transactions
        self.verify_transactions(image_contents, result.model_dump())
        
        return result
        
    def verify_transactions(self, image_contents, extracted_json):
        verify_prompt = """
        I will provide you with bank statement images and a JSON of extracted transactions.
        Please compare the original images with the extracted data and provide a detailed analysis of any discrepancies found.
        
        Focus on:
        1. Missing transactions
        2. Incorrect dates
        3. Incorrect descriptions (even minor differences)
        4. Incorrect values
        5. Incorrect balances
        6. Wrong order of transactions
        
        If you find any differences, explain them clearly. If everything matches perfectly, state that.
        
        Extracted JSON:
        {json_str}
        
        Please analyze the images and provide a detailed comparison report.
        """.format(json_str=json.dumps(extracted_json, indent=2))
        
        message = HumanMessage(
            content=[
                {"type": "text", "text": verify_prompt},
                *image_contents
            ]
        )
        
        verification_result = self.verify_model.invoke([message])
        print("\nVerification Report:")
        print(verification_result.content)