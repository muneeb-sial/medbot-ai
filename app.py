from fastapi import FastAPI
from app_collections.book_collection import get_book_collection
from jobs.bulk_insert import read_dir
import asyncio
from services.book_service import BookService
from services.llm_service import LlmService
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)   

book_collection = get_book_collection()

# asyncio.create_task(read_dir("./books/batch-1"))

@app.get("/")
def read_root():
    return {"message": "Hello World"}

# @app.get("/query",)
# def read_root():
#     obj = BookService()
#     query = "what if Adult Still disease"
#     books = obj.get_relevevant_books(query)
#     return {"data": books}

# @app.get("/id",)
# def read_root2(id: str):
#     obj = BookService()
#     books = obj.get_documents_by_doc_ids([id])
#     return {"data": books}

@app.get("/llm")
def read_root3(query: str):
    print("LLM called")
    obj = LlmService()
    return obj.chat_with_documents_streaming_output(query)

