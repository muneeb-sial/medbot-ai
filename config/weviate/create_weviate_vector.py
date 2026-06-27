from pydantic import BaseModel
from pydantic import ValidationError
from config.vector_store_client.weviate import weviate_db_client
from typing import TypeVar
from config.embeddings.sentense_transformer import embedding
from langchain_text_splitters import RecursiveCharacterTextSplitter

Tokenizer = embedding
T = TypeVar("T", bound=BaseModel)


def chunk_text(text: str, chunk_size: int = 1000, chunk_overlap: int = 120):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    return splitter.split_text(text)


def create_weviate_db_vector(
    collection_name: str,
    data: T
):
    try:
        if not weviate_db_client.is_live():
            raise ConnectionError("Weaviate instance is not live.")
        print(f"🚧 Creating {collection_name} instance record")
        chunk_and_insert(data, collection_name) 
        print(f"✅ {collection_name} vector creation completed")
    except ValidationError as e:
         print("❌ Invalid data:", e.errors())  

def create_vector(text:str)-> list[float]:
    print("🚧 Creating vector for text")
    vector = Tokenizer.encode(text, normalize_embeddings=True).tolist()
    print("✅ Vector created successfully")
    return vector

def prepare_data(data: dict) -> str:
    return "\n\n".join(f"{k}\n {v}" for k, v in data.items())

def chunk_and_insert(data: T,collection_name: str):
        text_data = prepare_data(data.model_dump())
        chunks = chunk_text(text_data)
        for text in chunks:
            payload ={
                **data.model_dump(),
                "content": text
            }  
            vector = create_vector(text_data)
            weviate_db_client.collections.get(collection_name).data.insert(
                properties=payload,
                vector=vector
            )