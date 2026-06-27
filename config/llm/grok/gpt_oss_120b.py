from langchain_groq import ChatGroq
from env import get_env

llm = ChatGroq(
    api_key=get_env("GROQ_LLM_API_KEY"),
    model="openai/gpt-oss-120b",
    temperature=0,
    max_tokens=(1024 * 4),
    max_retries=2,
)
