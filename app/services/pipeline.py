from .data_input import DataInput
from ..config import Config
from pathlib import Path
from typing import Dict, Any
from langchain_unstructured import UnstructuredLoader
from langchain_core.messages import HumanMessage
import base64
import io
import fitz
from PIL import Image
from langchain.chat_models import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings
from IPython.display import HTML, display


class Pipeline:
    def __init__(self, config: Config):
        self.config = config
        self.llm = ChatOpenAI(
            model="gpt-4-vision-preview",
            api_key=config.llm_api_key,
            base_url=config.llm_api_url
        )

    def pdf_page_to_base64(self, pdf_path: str, page_number: int) -> str:
        """Convert a PDF page to a base64-encoded image."""
        pdf_document = fitz.open(pdf_path)
        page = pdf_document.load_page(page_number - 1)  # input is one-indexed
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode("utf-8")

    def process_file(self, file_path: Path) -> Dict[str, Any]:

        # Simple and fast text extraction
        loader = PyPDFLoader(file_path)
        pages = []
        for page in loader.alazy_load():
            pages.append(page)

        print(f"{pages[0].metadata}\n")
        print(pages[0].page_content)

        # Vector search
        # OPENAI_API_KEY
        vector_store = InMemoryVectorStore.from_documents(pages, OpenAIEmbeddings())
        docs = vector_store.similarity_search("What is LayoutParser?", k=2)
        for doc in docs:
            print(f'Page {doc.metadata["page"]}: {doc.page_content[:300]}\n')

        # Layout analysis and extraction of text from images
        # UNSTRUCTURED_API_KEY
        loader = UnstructuredLoader(
            file_path=file_path,
            strategy="hi_res",
            partition_via_api=True,
            coordinates=True,
        )
        docs = []
        for doc in loader.lazy_load():
            docs.append(doc)

        first_page_docs = [doc for doc in docs if doc.metadata.get("page_number") == 1]

        for doc in first_page_docs:
            print(doc.page_content)

        segments = [
            doc.metadata
            for doc in docs
            if doc.metadata.get("page_number") == 5 and doc.metadata.get("category") == "Table"
        ]

        display(HTML(segments[0]["text_as_html"]))

        conclusion_docs = []
        parent_id = -1
        for doc in docs:
            if doc.metadata["category"] == "Title" and "Conclusion" in doc.page_content:
                parent_id = doc.metadata["element_id"]
            if doc.metadata.get("parent_id") == parent_id:
                conclusion_docs.append(doc)

        for doc in conclusion_docs:
            print(doc.page_content)

        return "??"
        # # Convert first page to image
        # base64_image = self.pdf_page_to_base64(str(file_path), 1)
        
        # # Create multimodal message for LLM
        # message = HumanMessage(
        #     content=[
        #         {
        #             "type": "text",
        #             "text": """Analyze this document and extract key financial information:
        #             1. What type of document is this? (e.g., receipt, invoice, statement)
        #             2. What is the total amount?
        #             3. What is the date?
        #             4. What is the description or purpose?
        #             5. Are there any categories or tags?
                    
        #             Format your response as a JSON object with these fields."""
        #         },
        #         {
        #             "type": "image_url",
        #             "image_url": {
        #                 "url": f"data:image/jpeg;base64,{base64_image}"
        #             },
        #         },
        #     ],
        # )
        
        # # Get response from LLM
        # response = self.llm.invoke([message])
        
        # print(response.content)
        # return {
        #     "file_path": str(file_path),
        #     "analysis": response.content
        # }

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
