
from config.vector_store_client.weviate import weviate_db_client
from config.weviate.weviate_base_collection import WeaviateCollection
from model.book_model import Book_Model
from langchain_weaviate import WeaviateVectorStore  
from config.embeddings.sentense_transformer import embedding

def create_book_collection():
    print("🚧 Creating book_collection in Weaviate")
    if weviate_db_client.is_live():
        WeaviateCollection(
            client = weviate_db_client,
            model  = Book_Model,
            name   = "book_collection"
        )

def get_book_collection() -> WeaviateVectorStore:
    if  weviate_db_client.is_live():
        print("✅ weviate is ready")
        
    print("✅ 1")
    collection = weviate_db_client.collections.exists("book_collection")
    print("✅ 2")
    if not collection:
        print("Collection 'book_collection' does not exist in Weaviate.")
        create_book_collection()
        
    return WeaviateVectorStore(
            client     = weviate_db_client,
            embedding  = embedding,
            index_name = "book_collection",   
            text_key   = "content"
        )