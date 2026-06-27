
from config.vector_store_client.weviate import weviate_db_client
from config.weviate.weviate_base_collection import WeaviateCollection
from model.document_model import Document_Model
from langchain_weaviate import WeaviateVectorStore  
from config.embeddings.sentense_transformer import embedding

def create_document_collection():
    print("🚧 Creating document_collection in Weaviate")
    if weviate_db_client.is_live():
        WeaviateCollection(
            client = weviate_db_client,
            model  = Document_Model,
            name   = "document_collection"
        )

def get_document_collection() -> WeaviateVectorStore:
    if  weviate_db_client.is_live():
        print("✅ weviate is ready")
    collection = weviate_db_client.collections.exists("document_collection")
    if not collection:
        print("Collection 'document_collection' does not exist in Weaviate.")
        create_document_collection()
        
    return WeaviateVectorStore(
            client     = weviate_db_client,
            embedding  = embedding,
            index_name = "document_collection",   
            text_key   = "content"
        )