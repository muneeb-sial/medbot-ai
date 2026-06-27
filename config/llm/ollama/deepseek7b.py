from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="deepseek-chat-7b:latest",
    temperature=0,
    top_p=1,
    top_k=1,
    repeat_penalty=1.0,
)
