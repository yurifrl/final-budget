from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_chroma import Chroma
from models import Models

class Chat:
    def __init__(self, config: Config):
        # Initialize the models
        models = Models()
        self.embeddings = models.embeddings_ollama
        self.llm = models.model_ollama

        # Initialize the vector store
        self.vector_store = Chroma(
            collection_name="documents",
            embedding_function=self.embeddings,
            persist_directory=config.db_folder,  # Where to save data locally
        )


    def retrieve(self, query: str):
        # Define the chat prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant. Answer the question based only the data provided."),
            ("human", "Use the user question {input} to answer the question. Use only the {context} to answer the question.")
        ])

        # Define the retrieval chain
        retriever = self.vector_store.as_retriever(kwargs={"k": 10})
        combine_docs_chain = create_stuff_documents_chain(
            self.llm, prompt
        )
        retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)

        return retrieval_chain.invoke({"input": query})

