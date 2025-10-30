from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import ChatPromptTemplate
from vectorstore import VectorStore
from utils import load_docs, docs_splitter

from dotenv import load_dotenv

load_dotenv()

class ChatBot:
    def __init__(self, doc_path, model_name="gemini-2.5-flash"):
        self.model = None
        self.vector_store = None

        self.conversation_memory = []
        self.model_name = model_name
        self.doc_path = doc_path
        self._init_chatbot()

    def _init_chatbot(self):
        print("🤖 Initializing Bot")
        try:
            self.model = ChatGoogleGenerativeAI(model=self.model_name, temperature=.7)
            self.vector_store = VectorStore() 
            splitted_docs = self._load_docs()
            self.vector_store.add_document(splitted_docs)
            print("🤖 Bot Initialized")
        except Exception as e:
            print(f"Failed to initialize bot: {e}")
            return

    def _load_docs(self):
        docs = load_docs(self.doc_path)
        splitted_docs = docs_splitter(docs)
        return splitted_docs
        

    def _create_context(self, query):
        similarities = self.vector_store.search(query, k=3) 
        

        for i, doc in enumerate(similarities):
            print(f"\nChunk {i+1}:")
            print(doc.page_content[:200])
        
        context = "\n\n".join([doc.page_content for doc in similarities])
        
        return context

    def chat(self, query):
        context = self._create_context(query)

        system_prompt = f"""You are a helpful assistant.
        Use this context to answer user queries:
        {context}
        """

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", "{query}")
        ])

        chain = prompt | self.model
        response = chain.invoke({"query": query})
        return response.content


    