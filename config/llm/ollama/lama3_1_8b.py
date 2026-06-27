from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="llama3.1:8b-instruct-q4_0",
    temperature=0,
    top_p=1,
    top_k=1,
    repeat_penalty=1.0,
)
