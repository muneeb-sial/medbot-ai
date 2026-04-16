from config.llm.Ollama.llama3 import llm
# from config.llm.Ollama.qwen25 import llm
from langchain.messages import HumanMessage, SystemMessage
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver  
from services.book_service import BookService
import json, random, asyncio
from fastapi.responses import StreamingResponse


class LlmService:
   def __init__(self):
        self.book_service = BookService()
        self.system_prompt = SystemMessage(
            content=(
                "You respond from provided context only. "
                "If the answer is not in the documents, say 'I don't know'. "
                "Respond in markdown."
            )
        )

        self.llm = llm          # injected or imported
        self.agent = create_agent(
            self.llm,
            checkpointer=InMemorySaver(),
        )
   
   def chat_with_documents_streaming_output(self, query: str):
        START = json.dumps({"status": "START"})
        END = json.dumps({"status": "END"})
        documents = self.book_service.get_relevevant_books(query)
        print(f"✔ Found {len(documents)} relevant documents.")
        documents = self.book_service.prepare_data_for_llm(docs=documents)
        print("="*50)
        print(f"✔ LLm ready{len(documents)} relevant documents.")
        print("="*50)
        human_message = HumanMessage(content=f"""Use the below context to answer the question.
        Context: {documents}
        Question: {query}
        Answer in markdown format.
        """)
        print(f"""Use the below context to answer the question.
        Context: {documents}
        Question: {query}
        Answer in markdown format.
        """)
        async def token_stream():
            yield f"data: {START}\n\n"
            full_text = ""
            stream = self.agent.stream(
                {"messages": [self.system_prompt, human_message]},
                {"configurable": {"thread_id": "1"}},
                stream_mode="messages",
            )
            try:
                for token ,_ in stream:
                    if token.content_blocks and len(token.content_blocks) > 0:
                        for block in token.content_blocks:
                            if "text" in block:
                                # print(block["text"], end='', flush=True)
                                response_chunk = json.dumps({"type": "chunk","status": "generating", "token": block["text"]})
                                yield f"data: {response_chunk}\n\n"
                                token = block["text"]
                                full_text += token
                                await asyncio.sleep(random.uniform(0.01, 0.1))
            except Exception as e:
                error_response = json.dumps({"type": "error", "message": str(e)})
                print({error_response})
                yield f"data: {error_response}\n\n"
            finally:
                response = json.dumps({"type": "text","status": "finished", "stream": full_text})
                yield f"data: {response}\n\n"
                yield f"data: {END}\n\n"

        return StreamingResponse(token_stream(), media_type="text/event-stream")
  