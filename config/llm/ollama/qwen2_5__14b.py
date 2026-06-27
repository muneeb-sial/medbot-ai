from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="qwen2.5-coder:14b",
    temperature=0,
    top_p=1,
    top_k=1,
    repeat_penalty=1.0,
)
