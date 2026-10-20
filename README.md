# 🩺 MedBot AI

**MedBot AI** is a FastAPI-powered conversational AI backend that combines a **LangGraph ReAct agent**, **Groq-hosted LLMs**, and a **Weaviate vector store** to deliver fast, context-aware, RAG-driven chat responses — streamed token-by-token over SSE.

---

## ✨ What it does

- 🤖 Runs an **agentic chatbot** (built with `langgraph`'s `create_react_agent`) that reasons about a user's query and decides when to call tools vs. answer directly.
- 🔍 Performs **semantic document search** over an ingested knowledge base using **HuggingFace sentence embeddings** (`all-MiniLM-L6-v2`) + **Weaviate**.
- ⚡ Streams responses in real time via **Server-Sent Events (SSE)**, including live tool-call and tool-result events.
- 🧠 Keeps **per-user conversational memory** using a LangGraph checkpointer, keyed by thread/user ID.
- 📥 Ingests `.txt` / `.md` documents from a directory, chunks them (`RecursiveCharacterTextSplitter`), and stores them as embedded vectors.
- 📨 Offloads document ingestion to a **background task queue** (`taskiq`) via publish/subscribe, keeping API responses fast.
- 🔌 Pluggable LLM backends — swap between **Groq** (`openai/gpt-oss-120b`) and local **Ollama** models (Llama 3.1, DeepSeek, Qwen2.5) with a one-line import change.

---

## 🏗️ Architecture

```
Client ──HTTP/SSE──▶ FastAPI (app.py)
                        │
                        ├── /chat routes ──▶ AgentService (LangGraph ReAct agent)
                        │                         │
                        │                         ├── LLM (Groq / Ollama)
                        │                         ├── Memory checkpointer
                        │                         └── document_search_tool
                        │                                   │
                        │                                   ▼
                        │                         DocumentService ──▶ Weaviate (vector store)
                        │
                        └── /job route ──▶ Taskiq broker ──▶ background document ingestion
```

---

## 📁 Project structure

```
app.py                      # FastAPI entrypoint
config/
  agent/                    # Agent, system prompt, memory, tools
  embeddings/                # HuggingFace embeddings factory
  llm/                       # LLM provider configs (Groq, Ollama)
  queue/                     # Taskiq broker, pub/sub jobs
  server/                    # FastAPI app config
  vector_store_client/       # Weaviate client
  weviate/                   # Weaviate collection setup
app_collections/             # Vector collection accessors
routes/                      # API route definitions
services/                    # Business logic (documents, LLM)
jobs/                        # Ingestion jobs (bulk/single insert)
data/                        # Source documents for ingestion
docker-compose.yml           # Weaviate + Weaviate UI services
```

---

## 🚀 Getting started

### 1. Prerequisites
- Python 3.10+
- Docker (for Weaviate)
- A [Groq API key](https://console.groq.com/)

### 2. Setup

```bash
# Clone and enter the project
cd medbot-ai

# Create a virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate # macOS/Linux

# Install dependencies
pip install -r req.txt

# Configure environment variables
cp .env.example .env
# then fill in GROQ_LLM_API_KEY and BE_SERVER_URL
```

### 3. Start Weaviate (vector store)

```bash
docker-compose up -d
```

This spins up:
- `weaviate` on `:8080` / `:50051`
- `weaviate-ui` on `:3000` for browsing collections

### 4. Run the API

```bash
python app.py
```

The server starts on `http://localhost:5001`.

---

## 🔌 API endpoints

| Method | Endpoint     | Description                                      |
|--------|--------------|---------------------------------------------------|
| GET    | `/`          | Health check                                       |
| GET    | `/job`       | Trigger a sample background document ingestion job |
| GET    | `/chat/e`    | Get a single agent response (non-streaming)        |
| GET    | `/chat/as`   | Stream agent responses + tool calls via SSE        |
| GET    | `/chat/s`    | Mock token-stream demo                             |

---

## 🌟 Why this project stands out

- ✅ **Agentic, not just retrieval** — uses a real ReAct loop so the bot decides *when* to search documents instead of always stuffing context blindly.
- ✅ **True streaming UX** — SSE events differentiate between generating tokens, tool calls, and tool results, enabling rich real-time UIs.
- ✅ **Swappable LLM layer** — cloud (Groq) and local (Ollama) models are interchangeable with a single import, great for cost control or offline development.
- ✅ **Decoupled ingestion pipeline** — document processing runs through a task queue instead of blocking API requests.
- ✅ **Conversational memory per user** — multi-turn context is preserved via thread-scoped checkpointing.
- ✅ **Lightweight, local-first embeddings** — no external embedding API costs thanks to `sentence-transformers`.

---

## 🛠️ Tech stack

`FastAPI` · `LangGraph` · `LangChain` · `Groq` · `Weaviate` · `HuggingFace Embeddings` · `Taskiq` · `Uvicorn` · `Docker`

---

## 📄 License

Not specified.
