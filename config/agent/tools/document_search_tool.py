from langchain.tools import tool
from aiocache import cached
from services.document_service import DocumentService


document_service = DocumentService()

@cached(ttl=60)
async def document_search(query):
    return document_service.get_relevevant_documents(query)

@tool(
    name_or_callable="document_search_tool",
    description="Search for documents based on a query string.",
)
async def document_search_tool(params):
    return await document_search(params)