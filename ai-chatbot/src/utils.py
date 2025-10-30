from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pydantic import BaseModel

class ChatBotData(BaseModel):
    query: str


def load_docs(docs_path):
    loader = PyPDFLoader(file_path=docs_path)
    docs = loader.load()
    return docs

def docs_splitter(docs, chunk_size=1000, chunk_overlap=200):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    spliited_docs = splitter.split_documents(docs)
    return spliited_docs