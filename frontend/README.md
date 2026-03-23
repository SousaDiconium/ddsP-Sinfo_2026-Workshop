# 🖥️ Frontend

> Streamlit dashboard for exploring the knowledge base, browsing documents and embeddings, visualizing vectors in 3D, and managing document tables.

[⬅️ Back to main README](../README.md)

---

## 🤔 What does it do?

This is the interactive face of the project. It connects to the [Knowledge Service](../knowledge_service/README.md) API and gives you a visual way to explore everything that's happening under the hood — from syncing vaults to querying knowledge to seeing embeddings projected into 3D space.

---

## 🚀 Running

Make sure the [Knowledge Service](../knowledge_service/README.md) is running first, then:

**Terminal:**
```bash
uv run streamlit run frontend/frontend/app.py
```

**VS Code:** Use the **"Frontend"** launch configuration (Ctrl+Shift+D).

The dashboard opens at [http://localhost:8501](http://localhost:8501).

---

## 📄 Pages

The dashboard has 5 pages, accessible via the sidebar:

### 🏠 Home

Welcome page with an architecture overview, API health check, and navigation cards to all other pages.

### 🧠 Knowledge Base

- **Document Tables** — See all indexed tables with their chunk counts
- **Obsidian Vaults** — View configured vault sources and trigger syncs
- **Query Knowledge** — Ask questions via semantic search with a configurable `top_k` slider (how many chunks to retrieve)

### 📄 Document Explorer

- **Browse Tables** — See chunk counts per table
- **Browse Sources** — Paginated list of source files within a table
- **Browse Chunks** — Inspect individual text chunks, their metadata, and embedding vectors (preview + stats)

### 🚀 Embedding Playground

- **Input Sentences** — Add 2-8 sentences with labels
- **3D Visualization** — See embeddings projected from 3072D to 3D via PCA, with lines colored by similarity
- **Similarity Scores** — Cosine similarity between every pair, with color-coded bars
- **Embedding Details** — Raw vector values, min/max/mean/std statistics per sentence

### 🗄️ Table Management

- **Create Table** — Create an empty document table
- **Delete Table** — Drop a table (with confirmation)
- **Upload Document** — Upload `.md`, `.txt`, or `.pdf` files for ingestion into a table

---

## 🎨 Theming

The dashboard uses a custom theme inspired by [SINFO](https://sinfo.org/) and [IST](https://tecnico.ulisboa.pt/):

- **Primary accent:** IST blue (`#009de0`)
- **Adaptive:** Works in both light and dark mode (uses semi-transparent colors)
- **Configured in:** [`.streamlit/config.toml`](./.streamlit/config.toml)
- **Custom CSS in:** [`frontend/utils/theme.py`](./frontend/utils/theme.py)

---

## 📂 Project Structure

```
frontend/
├── .streamlit/
│   └── config.toml               # Streamlit theme configuration
├── frontend/
│   ├── __init__.py
│   ├── app.py                     # Home page (entry point)
│   ├── pages/
│   │   ├── 1_Knowledge_Base.py    # Vault sync + semantic search
│   │   ├── 2_Document_Explorer.py # Browse tables, sources, chunks
│   │   ├── 3_Embedding_Playground.py # 3D visualization + similarity
│   │   └── 4_Table_Management.py  # Create, delete, upload
│   └── utils/
│       ├── api.py                 # HTTP client for the knowledge service
│       ├── layout.py              # Shared page setup + sidebar branding
│       └── theme.py               # Custom CSS + color constants
├── pyproject.toml
└── README.md                      # You are here
```

### How Streamlit multi-page apps work

Streamlit automatically creates URL-based navigation from files in the `pages/` directory. The numeric prefix (`1_`, `2_`, etc.) controls the order in the sidebar. Each page is a standalone Python script that runs top-to-bottom. Shared setup (theme, sidebar branding) is handled by [`utils/layout.py`](./frontend/utils/layout.py).

---

## 🧰 Key Dependencies

| Package | Purpose |
|---|---|
| `streamlit` | Web dashboard framework |
| `plotly` | Interactive 3D scatter plots for embedding visualization |
| `requests` | HTTP client for the knowledge service API |
| `numpy` | Vector math for embeddings |
| `scikit-learn` | PCA dimensionality reduction (3072D → 3D) |

---

## 📦 Installing Dependencies

All dependencies are managed from the **project root**:

```bash
# From the repo root
uv sync --all-packages
```

---

## 🛠️ Development

Run these from inside the `frontend/` directory:

```bash
# Format + lint (auto-fix)
uv run ruff format && uv run ruff check --fix

# Type check
uv run mypy .
```

---

[⬅️ Back to main README](../README.md)
