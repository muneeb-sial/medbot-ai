from app_collections.documents_collection import get_document_collection
from datetime import datetime
from langchain_text_splitters import RecursiveCharacterTextSplitter
import uuid
from langchain_core.documents import Document
import os

document_collection = get_document_collection()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

async def insert_one_with_filepath(path: str):
    docs = []
    
    if os.path.isfile(path) and path.endswith((".txt", ".md")):
        with open(path, "r", encoding="utf-8") as f:
            
            content = f.read()
            texts = splitter.split_text(content)
            book_doc_id = str(uuid.uuid4())
            now = datetime.utcnow().isoformat()
            
            for idx, chunk in enumerate(texts):
                chunk_id = str(uuid.uuid4())
                metadata = {
                    "doc_id": book_doc_id,
                    "chunk_id": chunk_id,
                    "chunk_index": idx,
                    "content": chunk,
                    "title": path,
                    "created_at": now,
                    "updated_at": now,
                }
                docs.append(Document(page_content=chunk, metadata=metadata))            
            print(f"✅ appended {path}")
    
    print(f"🚧 Total documents to add: {len(docs)}")
    
    for doc in docs:
        print("🚧 adding document with metadata:", doc.metadata)
        await document_collection.aadd_documents([doc])
        print("✅ added document with metadata:", doc.metadata)
        
    print(f"Inserted documents into book collection.")