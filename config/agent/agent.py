import json
from typing import Optional

# from config.llm.ollama.lama3_1_8b import llm
# from config.llm.ollama.deepseek7b import llm
# from config.llm.ollama.qwen2_5__14b import llm
from config.llm.grok.gpt_oss_120b import llm

# from langchain.agents import create_agent
from langgraph.prebuilt import create_react_agent
from config.agent.system_prompt import system_prompt
from config.agent.memory import checkpointer
from langchain.messages import HumanMessage
from config.agent.tools.tools import tools
from langchain_core.messages.ai import AIMessageChunk


class AgentService:
    def __init__(
        self,
        llm=llm,
        tools: list | None = tools,
        name: str | None = None,
    ):
        print("🚧 Initializing AgentService...")
        self.agent = create_react_agent(
            model=llm,
            tools=tools,
            name=name or "default-agent",
            checkpointer=checkpointer,
            prompt=system_prompt,
        )
        print("✅ AgentService initialized.")

    async def arun(self, query: str, user_id: Optional[int] | None) -> str:
        config = {"configurable": {"thread_id": f"user-{user_id or 'unknown'}"}}
        response = await self.agent.ainvoke(
            {"messages": [HumanMessage(content=query)]},
            config=config,
        )
        return response["messages"][-1].content

    async def astream(self, query: str, user_id: Optional[int] | None):
        config = {"configurable": {"thread_id": f"user-{user_id or 'unknown'}"}}
        async for event in self.agent.astream(
            {"messages": [HumanMessage(content=query)]},
            config=config,
            stream_mode="messages",
        ):
            yield event

    async def astream_generator_raw(self, query: str, user_id: Optional[int] | None):

        async for chunk, meta in self.stream(query, user_id):
            chunk = AIMessageChunk.model_dump(chunk)
            data = {**chunk, **meta}
            yield f"data: {json.dumps(data)}\n\n"

    async def _astream_generator_content(
        self, query: str, user_id: Optional[int] | None
    ):
        try:
            yield f"data: {json.dumps({'status': 'START'})}\n\n"
            async for chunk, meta in self.astream(query, user_id):
                chunk = AIMessageChunk.model_dump(chunk)

                data = {
                    "status": "GENERATING",
                    "type": "chunk",
                    "token": chunk["content"],
                    "tool_calls": chunk.get("tool_calls", []),
                    "invalid_tool_calls": chunk.get("invalid_tool_calls", []),
                }

                if chunk.get("tool_calls"):
                    print("TOOL CALL")
                    print("TOOL CALL META:")
                    print(json.dumps(meta, indent=2, default=str))

                    print("\nTOOL CALL CHUNK:")
                    print(json.dumps(chunk, indent=2, default=str))
                    tool_data = {
                        "status": "TOOL_CALL",
                        "type": "tool_call",
                        "tool": chunk["tool_calls"][0]["name"],
                        "args": chunk["tool_calls"][0]["args"],
                        "call_id": chunk["tool_calls"][0]["id"],
                    }
                    yield f"data: {json.dumps(tool_data)}\n\n"
                    continue

                if meta.get("langgraph_node") == "tools":
                    print("langgraph_node")
                    print("langgraph_node META:")
                    print(json.dumps(meta, indent=2, default=str))

                    print("\nlanggraph_node CHUNK:")
                    print(json.dumps(chunk, indent=2, default=str))

                    data.pop("token", None)
                    data["tool_calls"] = [chunk.get("content")]
                    data["type"] = "tool_calls"
                    yield f"data: {json.dumps(data)}\n\n"
                    continue

                if chunk["content"] == "":
                    continue

                # yield f"data: {json.dumps(data)}\n\n"
            yield f"data: {json.dumps({'status': 'END'})}\n\n"
        except Exception as e:
            error_response = json.dumps(
                {"status": "END", "type": "error", "message": str(e)}
            )
            yield f"data: {error_response}\n\n"

    async def astream_generator_content(
        self, query: str, user_id: Optional[int] | None
    ):
        pending_tools = {}

        try:
            yield f"data: {json.dumps({'status': 'START'})}\n\n"

            async for chunk, meta in self.astream(query, user_id):
                chunk = AIMessageChunk.model_dump(chunk)

                # ----------------------------
                # TOOL CALL DETECTED
                # ----------------------------
                if chunk.get("tool_calls"):
                    for tool_call in chunk["tool_calls"]:
                        pending_tools[tool_call["id"]] = {
                            "id": tool_call["id"],
                            "name": tool_call["name"],
                            "args": tool_call["args"],
                        }

                    continue

                # ----------------------------
                # TOOL RESULT DETECTED
                # ----------------------------
                if meta.get("langgraph_node") == "tools":
                    tool_call_id = chunk.get("tool_call_id")

                    if tool_call_id and tool_call_id in pending_tools:
                        tool_info = pending_tools.pop(tool_call_id)

                        tool_event = {
                            "status": "TOOL_EXECUTED",
                            "type": "tool_execution",
                            "tool_id": tool_info["id"],
                            "tool_name": tool_info["name"],
                            "input": tool_info["args"],
                            "output": chunk.get("content"),
                            "tool_status": chunk.get("status", "success"),
                        }

                        yield f"data: {json.dumps(tool_event)}\n\n"

                    continue

                # ----------------------------
                # NORMAL TOKEN STREAM
                # ----------------------------
                if chunk.get("content"):
                    data = {
                        "status": "GENERATING",
                        "type": "chunk",
                        "token": chunk["content"],
                    }

                    yield f"data: {json.dumps(data)}\n\n"

            yield f"data: {json.dumps({'status': 'END'})}\n\n"

        except Exception as e:
            yield (
                f"data: "
                f"{json.dumps({'status': 'END', 'type': 'error', 'message': str(e)})}"
                f"\n\n"
            )

    def delete_memory(self, thread_id: str):
        checkpointer.delete_thread(thread_id)
