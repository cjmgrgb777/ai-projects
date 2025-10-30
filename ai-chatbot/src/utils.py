from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pydantic import BaseModel


class ChatBotData(BaseModel):
    query: str


def load_docs(docs_path):
    loader = PyPDFLoader(file_path=docs_path)
    docs = loader.load()
    
    for doc in docs:
        text = doc.page_content
        
        import re
        pattern = r"\n\s*REFERENCES\s*\n[\s\S]*"
        
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        
        if "Abbas" in text or "et al." in text:
            print("WARNING: References still found in document!")
            print(f"Last 200 chars: {text[-200:]}")
        else:
            print("References successfully removed")
        
        doc.page_content = text
        
    return docs

def docs_splitter(docs, chunk_size=1000, chunk_overlap=200):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    spliited_docs = splitter.split_documents(docs)
    return spliited_docs