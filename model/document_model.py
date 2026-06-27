from pydantic import BaseModel

class Document_Model(BaseModel):
    doc_id: str
    chunk_id: str
    chunk_index: int
    title: str
    content: str
    created_at: str
    updated_at: str