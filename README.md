# Docu-Mind

A full-stack RAG (Retrieval-Augmented Generation) pipeline that lets you upload PDF and text documents and chat with them using natural language.

## Architecture

```
User → Streamlit UI → FastAPI Backend → LangGraph RAG Pipeline
                                      ↓
                            pgvector (PostgreSQL)
                                      ↑
                         Gemini Embeddings API
```

**RAG Flow:**
1. Document uploaded → parsed into chunks → embedded via Gemini → stored in pgvector
2. Question asked → embedded → similar chunks retrieved (cosine similarity) → Gemini generates answer with context + chat history

## Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | FastAPI |
| RAG Orchestration | LangGraph |
| Embeddings & LLM | Google Gemini API (`gemini-embedding-001`, `gemini-3.1-flash-lite-preview`) |
| Vector Store | PostgreSQL + pgvector |
| Document Parsing | pymupdf4llm, LangChain text splitters |

## Project Structure

```
docu-mind/
├── app/
│   ├── main.py          # FastAPI routes (/upload, /ask)
│   ├── parser.py        # PDF + TXT chunking (RecursiveCharacterTextSplitter)
│   ├── embeddings.py    # Gemini embedding generation + pgvector storage/search
│   ├── rag.py           # LangGraph pipeline (retrieve → generate → memory)
│   └── db.py            # PostgreSQL connection
├── frontend/
│   └── streamlit_app.py # Chat UI with file uploader
├── docker/
│   └── docker-compose.yaml  # pgvector service
├── documents/           # Uploaded documents stored here
├── k8s/                 # Kubernetes manifests (KIND)
├── terraform/           # AWS infrastructure (coming soon)
└── evaluation/          # RAGAS eval metrics (coming soon)
```

## Getting Started

### Prerequisites

- Python 3.12+
- Docker
- A Google Gemini API key

### 1. Start the database

```bash
cd docker
docker compose up -d
```

This starts PostgreSQL with the pgvector extension on port `5432`.

### 2. Set up the environment

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
API_KEY=your_gemini_api_key_here
```

### 3. Run the backend

```bash
uvicorn app.main:app --reload
```

API available at `http://localhost:8000`

### 4. Run the frontend

```bash
streamlit run frontend/streamlit_app.py
```

UI available at `http://localhost:8501`

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Health check |
| `POST` | `/upload` | Upload PDF/TXT files for processing |
| `POST` | `/ask` | Ask a question with optional chat history |

## Roadmap

- [x] PostgreSQL + pgvector setup
- [x] Document parser (PDF + TXT)
- [x] Gemini embeddings pipeline
- [x] LangGraph RAG orchestration
- [x] FastAPI backend
- [x] Streamlit frontend
- [ ] Dockerize full stack (FastAPI + Streamlit)
- [ ] Deploy on KIND (local Kubernetes)
- [ ] Terraform + AWS EKS deployment
- [ ] GitHub Actions CI/CD
- [ ] Ollama integration (self-hosted LLM)
- [ ] RAGAS evaluation metrics
