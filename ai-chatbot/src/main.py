from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# helpers
from utils import ChatBotData, load_docs, docs_splitter

# agent
from chatbot import ChatBot


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_methods=["*"],
    allow_credentials=True
)

@app.get("/")
def index():
    response = {
        "message": "Hello World"
    }

    return response

@app.post("/chatbot")
def chat_bot(query: ChatBotData):
    bot = ChatBot(doc_path="./data/pdfs/Role_of_AI_in_Education.pdf")
    
    while True:
        text = input("User: ")
        bot_response = bot.chat(text)
        print(f"Bot: {bot_response}")