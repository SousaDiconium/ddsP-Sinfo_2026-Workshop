# 🧠 Knowledge Service

> FastAPI backend that powers the RAG (Retrieval-Augmented Generation) pipeline — ingests documents, generates embeddings via Azure OpenAI, stores them in PostgreSQL + pgvector, and provides semantic search.

[⬅️ Back to main README](../README.md)

---

## 🤔 What does it do?

This is the brain of the project. It takes documents (from Obsidian vaults, file uploads, or agent ingestion), splits them into chunks, converts each chunk into a 3072-dimensional embedding vector, and stores everything in a PostgreSQL database with the pgvector extension. When you ask a question, it embeds your query and finds the most similar document chunks using cosine similarity.

```
Documents (.md, .txt, .pdf)
  → DocumentSplitter (100-word chunks, 30-word overlap)
    → AzureOpenAIDocumentEmbedder (text → 3072-dim vector)
      → PgvectorDocumentStore (PostgreSQL + pgvector)
        → PgvectorEmbeddingRetriever (cosine similarity search)
          → Ranked results with sources
```

---

## ✅ Prerequisites

| Tool | Why |
|---|---|
| **Docker** | Runs PostgreSQL + pgvector locally |
| **Azure OpenAI access** | Generates embedding vectors (provided during the workshop) |

---

## 🚀 Setup & Running

### 1. Start PostgreSQL

From the **project root**:

```bash
docker compose up -d
```

This starts a PostgreSQL 16 instance with pgvector on port 5432. See [`docker-compose.yml`](../docker-compose.yml).

### 2. Configure environment

```bash
cp knowledge_service/resources/.env.example knowledge_service/resources/.env
```

Fill in your Azure OpenAI credentials. See [`.env.example`](./knowledge_service/resources/.env.example) for all required variables.

### 3. Run the service

**Terminal:**
```bash
uv run uvicorn knowledge_service.main:app --reload
```

**VS Code:** Use the **"Knowledge Service"** launch configuration (Ctrl+Shift+D).

The API is available at:
- **API:** [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Swagger docs:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📡 API Endpoints

### 🏠 General

| Method | Path | Description |
|---|---|---|
| `GET` | `/` | Welcome message / health check |

### 📚 Obsidian Vaults

| Method | Path | Description |
|---|---|---|
| `GET` | `/obsidian-vaults` | List all configured vaults |
| `GET` | `/obsidian-vaults/{vault_id}/sync` | Trigger vault sync (index all files) |

### 📄 Documents

| Method | Path | Description |
|---|---|---|
| `GET` | `/document-tables` | List all document tables with chunk counts |
| `POST` | `/document-tables` | Create an empty document table |
| `DELETE` | `/document-tables/{table_name}` | Delete a document table |
| `POST` | `/document-tables/{table_name}/documents` | Upload a file for ingestion (.md, .txt, .pdf) |
| `POST` | `/document-tables/{table_name}/knowledge` | Query knowledge via semantic search |
| `GET` | `/document-tables/{table_name}/sources` | List sources in a table (paginated) |
| `GET` | `/document-tables/{table_name}/sources/{source_id}/documents` | List document chunks (paginated) |

### 🔢 Embeddings

| Method | Path | Description |
|---|---|---|
| `POST` | `/embeddings` | Generate embedding for a single text |
| `POST` | `/embeddings/compare` | Embed multiple texts + compute cosine similarity |

### 🧪 Testing with .http files

The [`requests/`](./requests/) directory contains ready-to-use HTTP request files:

| File | What it covers |
|---|---|
| [`welcome.http`](./requests/welcome.http) | Health check |
| [`obsidian-vaults.http`](./requests/obsidian-vaults.http) | Vault listing and sync |
| [`documents.http`](./requests/documents.http) | Table CRUD, file upload, knowledge queries |
| [`embeddings.http`](./requests/embeddings.http) | Embedding generation and comparison |

Open these in VS Code with the [REST Client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) extension and click "Send Request" to test each endpoint.

---

## 💡 Key Concepts for Students

### Document Chunking
Documents are split into overlapping windows of ~100 words (with 30-word overlap). This ensures each chunk is small enough to embed meaningfully while maintaining context across chunk boundaries.

### Embeddings
Text is converted into a 3072-dimensional vector using Azure OpenAI's `text-embedding-3-large` model. These vectors capture the *meaning* of text — similar text produces similar vectors.

### Vector Similarity
When you query, your question is also embedded into a vector. PostgreSQL + pgvector finds the stored chunks whose vectors are closest to your query vector using cosine similarity. This is called **semantic search** — it finds meaning, not just keywords.

### RAG Pipeline
Retrieval-Augmented Generation combines vector search (retrieval) with a language model (generation). First retrieve relevant chunks, then use them as context for the LLM to generate a grounded answer with real sources.

---

## ⚙️ Configuration

### [`resources/config.yaml`](./knowledge_service/resources/config.yaml)

Configures the Obsidian vault sources:

```yaml
log_level: DEBUG
obsidian_sources:
  - id: sinfo-generic
    location: ../../../obsidian-vaults/test-sinfo-vault
    description: General information about Sinfo...
  - id: sinfo-fenix
    location: ../../../obsidian-vaults/test-sinfo-fenix-vault
    description: Academic information scraped from Fenix...
```

### [`resources/.env`](./knowledge_service/resources/.env.example)

Required environment variables:

| Variable | Description |
|---|---|
| `AZURE_OPENAI_EMBEDDINGS_API_KEY` | Azure OpenAI API key |
| `AZURE_OPENAI_EMBEDDINGS_API_VERSION` | API version (default: `2024-12-01-preview`) |
| `AZURE_OPENAI_EMBEDDINGS_ENDPOINT` | Azure endpoint URL |
| `AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME` | Deployment name (default: `text-embedding-3-large`) |
| `AZURE_OPENAI_EMBEDDINGS_EMBEDDING_DIMENSION` | Embedding dimensions (default: `3072`) |
| `POSTGRES_CONNECTION_STRING` | PostgreSQL connection string |

---

## 📂 Project Structure

```
knowledge_service/
├── knowledge_service/
│   ├── __init__.py              # Service initialization
│   ├── main.py                  # FastAPI app + all endpoints
│   ├── models/                  # Pydantic DTOs
│   │   ├── answer.py            # Knowledge answer response
│   │   ├── document.py          # Document chunk model
│   │   ├── document_source.py   # Document source model
│   │   ├── document_table.py    # Table + create/upload DTOs
│   │   ├── embedding.py         # Embedding request/response DTOs
│   │   ├── message.py           # Generic message DTO
│   │   ├── query.py             # Knowledge query DTO (with top_k)
│   │   └── vault_info.py        # Vault info DTO
│   ├── services/
│   │   ├── ai_service.py        # Haystack AI pipelines (embed, split, search)
│   │   └── db_service.py        # PostgreSQL operations (tables, sources, documents)
│   ├── loaders/
│   │   └── obsidian_loader.py   # File loader (.md, .txt, .pdf → Haystack Document)
│   ├── jobs/
│   │   └── sync_obsidian.py     # Async vault sync job
│   ├── resources/
│   │   ├── config.yaml          # Vault source configuration
│   │   ├── .env.example         # Environment variables template
│   │   └── .env                 # Your credentials (gitignored)
│   └── utils/
│       ├── settings.py          # Settings loader (YAML + env)
│       └── logger.py            # Loguru setup
├── requests/                    # .http files for API testing
├── pyproject.toml
└── README.md                    # You are here
```

---

## 📦 Installing Dependencies

All dependencies are managed from the **project root**:

```bash
# From the repo root
uv sync --all-packages
```

---

## 🛠️ Development

Run these from inside the `knowledge_service/` directory:

```bash
# Format + lint (auto-fix)
uv run ruff format && uv run ruff check --fix

# Type check
uv run mypy .
```

---

[⬅️ Back to main README](../README.md)
