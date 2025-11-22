from fastapi import FastAPI
from app_collections.book_collection import get_book_collection
app = FastAPI()

book_collection = get_book_collection()
book_collection.aadd_texts(["This is a sample book content for testing the Weaviate vector store integration."])
@app.get("/")
def read_root():
    return {"message": "Hello World"}