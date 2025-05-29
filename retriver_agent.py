#!/usr/bin/env python
# coding: utf-8

# In[1]:


from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain.vectorstores import FAISS


class RetrieverAgent:
    def __init__(self, model_name="llama3.2:1b"):
        self.embedding_model = OllamaEmbeddings(model=model_name)

    def get_retriever(self, pdf_path: str):
        """
        Loads a PDF, splits it, embeds it, and returns a retriever.

        Args:
            pdf_path (str): Path to the PDF file.

        Returns:
            retriever: LangChain retriever object.
        """
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()

        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        split_docs = splitter.split_documents(documents)

        vector_store = FAISS.from_documents(split_docs, self.embedding_model)
        return vector_store.as_retriever()

# from agents.retriever_agent import RetrieverAgent

# retriever_agent = RetrieverAgent()
# retriever = retriever_agent.get_retriever("your_pdf_path_here.pdf")

