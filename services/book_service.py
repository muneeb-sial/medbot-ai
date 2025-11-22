from app_collections.book_collection import get_book_collection
from weaviate.classes.query import Filter

class BookService:
    def __init__(self):
        self.book_store = get_book_collection()
        
    def get_relevevant_books(self, user_query):
       if not user_query:
           raise ValueError("User query cannot be empty")
       docs = self.book_store.similarity_search(user_query ,k=10)
       return self.prepare_data_for_response(docs)
   
    def prepare_data_for_response(self, docs):
       documents = []
       for doc in docs:
        documents.append({
            "title": doc.metadata.get("title", "N/A"),
            "doc_id": doc.metadata.get("doc_id", "N/A"),
            "content": doc.page_content,
        })
       return documents

    def get_documents_by_doc_ids(self, doc_ids):
        if not doc_ids:
            raise ValueError("Document IDs list cannot be empty")
        docs = self.book_store.similarity_search(
            query = "*",
            k=100,
              filters=Filter.by_property("doc_id").contains_any(doc_ids)
            )
        return self.prepare_data_for_response(docs)
    
    def prepare_data_for_llm(self, docs):
       documents = []
       for doc in docs:
           data = f"""
           Title: {doc.get("title", "N/A")}
           Content: {doc.get("content", "N/A")}
         """
           documents.append(data)
       return "\n".join(documents)
