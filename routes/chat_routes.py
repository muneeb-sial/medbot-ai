import json
import random
import time
from fastapi.responses import StreamingResponse
from fastapi import APIRouter
from config.agent.agent import AgentService
from langchain_core.messages.ai import AIMessageChunk

chat_router = APIRouter()

chat_router.prefix = "/chat"
chat_router.tags = ["chat"]

agent = AgentService()


res = """

You are an enthusiastic and helpful salesperson. When a user asks about a product, your job is to respond in an engaging and informative way.

📝 **Instructions**:
- Use only the provided context to answer.
- If a relevant product exists in the context, briefly pitch it.
- After the pitch, create a **Markdown table** showing details of the product.
- Your entire response must be in **Markdown format**.
- At the end of your response ask if the like to know more or are they interested in any other product.

📚 **Context** (choose the most relevant product info based on the question):
"""


async def chat(query: str = ""):
    START = json.dumps({"status": "START"})
    END = json.dumps({"status": "END"})

    async def token_stream():
        yield f"data: {START}\n\n"
        try:
            # response = chain.invoke({"context": context, "question": query})
            response = res + "\n\n" + query
            for i in range(0, len(response), 10):
                chunk = response[i : i + 10]
                reponse_chunk = json.dumps({"type": "chunk", "token": chunk})
                yield f"data: {reponse_chunk}\n\n"
                time.sleep(random.uniform(0.01, 0.1))

        except Exception as e:
            error_response = json.dumps({"type": "error", "message": str(e)})
            yield f"data: {error_response}\n\n"
        yield f"data: {END}\n\n"

    return StreamingResponse(token_stream(), media_type="text/event-stream")

@chat_router.get("/s")
async def chat_stream(query: str = ""):
    return await chat(query)

@chat_router.get("/e")
async def chat_endpoint(query: str = "need you tro find product with id 1 and tell me its name?"):
    response = await agent.arun(query,1)
    return response

@chat_router.get("/as")
async def chat_agent_stream(query: str = "Need to find a product with id 1 and tell me about it"):
    return StreamingResponse(
         agent.astream_generator_content(query, 1),
         media_type="text/event-stream",
    )