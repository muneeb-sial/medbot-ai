from dotenv import load_dotenv
load_dotenv()

from config.server.fastapi import app
from app_collections.documents_collection import get_document_collection
from routes.chat_routes import chat_router


book_collection = get_document_collection()


@app.get("/")
def read_root():
    return {"message": "healthy!"}


app.include_router(chat_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        port=5001,
        log_level="info",
        reload=True,
    )
