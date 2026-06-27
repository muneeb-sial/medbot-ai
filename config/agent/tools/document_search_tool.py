from langchain.tools import tool
from aiocache import cached

@cached(ttl=60)
async def document_search(query):
    pass

@tool(
    name_or_callable="document_search_tool",
    description="Search for documents based on a query string.",
)
async def document_search_tool(params):
    return await document_search(params)