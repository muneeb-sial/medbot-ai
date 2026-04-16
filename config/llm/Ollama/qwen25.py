from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="qwen2.5-coder:14b",
    temperature=0,
    top_p=1,            # full token space → prevents truncation randomness
    repeat_penalty=1.0, # remove extra penalty randomness
    num_ctx=8192,
    num_predict=512, 
)