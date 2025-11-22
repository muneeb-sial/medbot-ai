from fastapi import FastAPI
from app_collections.book_collection import get_book_collection
from jobs.bulk_insert import read_dir
import asyncio
app = FastAPI()

book_collection = get_book_collection()

# asyncio.create_task(read_dir("./books/batch-1"))

book_collection.aadd_texts(["This is a sample book content for testing the Weaviate vector store integration."])
@app.get("/")
def read_root():
    return {"message": "Hello World"}