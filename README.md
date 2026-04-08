# 🪶 Trivial Fenix - SINFO 33 Workshop

> **AI-Powered Knowledge Assistant** - Built by [diconium](https://diconium.com) for [SINFO 33](https://sinfo.org) at [Instituto Superior Tecnico](https://tecnico.ulisboa.pt), April 2026.

This project demonstrates how to build an AI-powered personal assistant that can scrape, index, and answer questions about academic content using **Retrieval-Augmented Generation (RAG)**.

Students will explore how text is chunked, embedded into high-dimensional vectors, stored in a vector database, and retrieved via semantic search, all through a hands-on dashboard and an AI agent.

---

## 🏗️ Architecture

```
Fenix Website
  → fenix_scraper (HTML → Markdown)
    → Obsidian Vault (.md files)
      → knowledge_service /sync (split → embed → store)
        → PostgreSQL + pgvector
          → knowledge_service /knowledge (semantic search)
            → Frontend Dashboard  or  OpenClaw Agent (Trivial Fenix 🪶)
              → You get answers with sources!
```

---

## 📂 Project Structure

This is a **Python 3.12 uv monorepo** with four workspace members:

| Directory | What it is | README |
|---|---|---|
| [`fenix_scraper/`](./fenix_scraper/) | CLI tool that scrapes Fenix and produces Obsidian vault files | [📖 README](./fenix_scraper/README.md) |
| [`knowledge_service/`](./knowledge_service/) | FastAPI backend — RAG engine with Haystack AI, Azure OpenAI, pgvector | [📖 README](./knowledge_service/README.md) |
| [`frontend/`](./frontend/) | Streamlit dashboard — explore documents, embeddings, and query knowledge | [📖 README](./frontend/README.md) |
| [`workspace-trivial-fenix-sinfo-2026/`](./workspace-trivial-fenix-sinfo-2026/) | OpenClaw AI agent workspace — the "Trivial Fenix" assistant | [📖 README](./workspace-trivial-fenix-sinfo-2026/README.md) |
| [`obsidian-vaults/`](./obsidian-vaults/) | Sample Obsidian vaults with SINFO info and scraped Fenix data | — |

---

## ✅ Prerequisites

Before starting, make sure you have:

| Tool | Version | Why |
|---|---|---|
| **Python** | 3.12 | The project requires Python 3.12 exactly |
| **[uv](https://docs.astral.sh/uv/)** | Latest | Fast Python package manager — manages the monorepo |
| **Docker** | Any recent version | Runs PostgreSQL + pgvector locally |
| **VS Code** | Recommended | Launch configs included for debugging |

You'll also need **Azure OpenAI credentials** for generating embeddings. During the workshop, these will be provided by diconium. After the workshop, the keys will be rotated — but everything you build here works with **any OpenAI-compatible provider** (OpenAI, Ollama, Mistral, etc.), and many of them have free tiers or student offers.

---

## 🚀 Quickstart

### 1. Clone the repo

```bash
git clone <repo-url>
cd ddsP-Sinfo_2026-Workshop
```

### 2. Install uv (if you don't have it)

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with Homebrew
brew install uv
```

### 3. Install all dependencies (from the root directory)

```bash
uv sync --all-packages
```

> **Important:** Always run this from the **project root**. It installs everything for all four workspace members into a single shared `.venv/`.

### 4. Set up environment variables

The knowledge service needs Azure OpenAI credentials and a PostgreSQL connection string.

```bash
# Copy the example and fill in your credentials
cp knowledge_service/knowledge_service/resources/.env.example \
   knowledge_service/knowledge_service/resources/.env
```

Edit the `.env` file and fill in the values. During the workshop, these will be provided.

### 5. Start PostgreSQL (Docker)

```bash
docker compose up -d
```

This starts a PostgreSQL instance with the pgvector extension on port 5432.

### 6. Start the Knowledge Service

```bash
uv run uvicorn knowledge_service.main:app --reload
```

The API will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000). You can also see the auto-generated docs at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

### 7. Start the Frontend

```bash
uv run streamlit run frontend/frontend/app.py
```

The dashboard will open at [http://localhost:8501](http://localhost:8501).

### 8. Explore!

- **Sync a vault** from the Knowledge Base page to index the sample Obsidian data
- **Ask questions** and see semantic search in action
- **Explore documents** to see how text is chunked and embedded
- **Play with embeddings** in the 3D visualization playground
- **Upload your own files** via Table Management

---

## 🖥️ VS Code

The project includes debug configurations in [`.vscode/launch.json`](./.vscode/launch.json):

| Configuration | What it starts |
|---|---|
| **Knowledge Service** | FastAPI backend with hot-reload via uvicorn |
| **Frontend** | Streamlit dashboard |

Use the **Run and Debug** panel (Ctrl+Shift+D / Cmd+Shift+D) to start either service with full debugging support.

---

## 🧰 Tech Stack

| Layer | Technologies |
|---|---|
| **Language** | Python 3.12 |
| **Package Management** | [uv](https://docs.astral.sh/uv/) (monorepo with workspaces) |
| **Backend API** | [FastAPI](https://fastapi.tiangolo.com/) |
| **RAG Pipeline** | [Haystack AI](https://haystack.deepset.ai/) |
| **Embeddings** | [Azure OpenAI](https://azure.microsoft.com/en-us/products/ai-services/openai-service) (`text-embedding-3-large`, 3072 dims) |
| **Vector Database** | [PostgreSQL](https://www.postgresql.org/) + [pgvector](https://github.com/pgvector/pgvector) |
| **Frontend** | [Streamlit](https://streamlit.io/) + [Plotly](https://plotly.com/python/) |
| **AI Agent** | [OpenClaw](https://openclaw.com/) |
| **Linting** | [Ruff](https://docs.astral.sh/ruff/) + [mypy](https://mypy-lang.org/) |
| **Scraping** | [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) + [html-to-markdown](https://pypi.org/project/html-to-markdown/) |

---

## 🎓 Workshop Modules

During the workshop you'll work through these concepts hands-on:

1. **📄 Document Chunking** — How large documents are split into overlapping ~100-word windows for embedding
2. **🔢 Embeddings** — How text is converted into 3072-dimensional vectors that capture meaning
3. **📐 Vector Similarity** — How cosine similarity finds relevant documents in pgvector
4. **🤖 RAG Pipeline** — How retrieval + generation work together to answer questions with real sources
5. **🌌 3D Visualization** — How PCA projects high-dimensional embeddings into an interactive 3D space
6. **🪶 AI Agent** — How the Trivial Fenix agent uses skills to browse, ingest, and answer questions autonomously

---

## 🔑 A Note on API Keys

During the workshop, Azure OpenAI credentials will be provided by **diconium**. These keys will be **rotated after the event**.

The good news: everything in this project is **provider-agnostic**. You can swap Azure OpenAI for:
- **OpenAI** directly
- **Ollama** (free, runs locally)
- **Mistral**, **Cohere**, or any other embedding provider supported by Haystack AI

Many providers offer **free tiers or student programs** — so you can keep experimenting after the workshop!

---

## 📜 License

Built by [diconium](https://diconium.com) for educational purposes at [SINFO 33](https://sinfo.org), Instituto Superior Tecnico, Lisbon.
