import faiss

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS

from dotenv import load_dotenv

load_dotenv()

class VectorStore:
    def __init__(self, model_name="gemini-embedding-001"):
        self.embeddings = None
        self.vector_store = None
        self.model_name = model_name
        self._init_store()
    
    def _init_store(self):
        self.embeddings = GoogleGenerativeAIEmbeddings(model=f"models/{self.model_name}", temperature=.7)

        embedding_dim = len(self.embeddings.embed_query("Hello, WOrld"))
        index = faiss.IndexFlatL2(embedding_dim)

        self.vector_store = FAISS(
            embedding_function=self.embeddings,
            docstore=InMemoryDocstore(),
            index=index,
            index_to_docstore_id={}
        )

    def add_document(self, docs):
        self.vector_store.add_documents(docs)

    def search(self, query, k=3):
        print(f"🔎 Searching from vector store...")
        results = self.vector_store.similarity_search(
            query=query,
            k=k
        )
        print(f"Found {len(results)} similarites")
        # for index, result in enumerate(results):
        #     print(f"{index + 1}. Source - {result.metadata.get("source")}\nContent: {result.page_content[:100]}") 
        
        return results