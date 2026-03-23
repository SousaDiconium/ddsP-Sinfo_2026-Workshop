# 🪶 Trivial Fenix — OpenClaw Agent Workspace

> AI agent workspace for the **Trivial Fenix** personal assistant, powered by [OpenClaw](https://openclaw.com/). This agent can browse Fenix, query the knowledge base, ingest documents, and help you explore academic content.

[⬅️ Back to main README](../README.md)

---

## 🤔 What is OpenClaw?

[OpenClaw](https://openclaw.com/) is a platform for building AI agents that can use tools, browse the web, run scripts, and interact with APIs. Think of it as an AI assistant that lives in a workspace full of instructions (skills) and can act on them autonomously.

The agent's personality, behavior, and capabilities are defined by markdown files in this workspace. No code required — just instructions.

---

## 🪶 Meet Trivial Fenix

| Field | Value |
|---|---|
| **Name** | Trivial Fenix |
| **Emoji** | 🪶 |
| **Vibe** | Resourceful, grounded, quick, casually witty |
| **Role** | Workshop demo companion for SINFO 33 |

The agent's identity is defined in [`IDENTITY.md`](./IDENTITY.md) and its behavior in [`SOUL.md`](./SOUL.md).

---

## 🛠️ Skills

Skills are the agent's capabilities. Each skill lives in its own directory under [`skills/`](./skills/) and is defined by a `SKILL.md` file with YAML frontmatter + markdown instructions.

| Skill | Description | User-invocable |
|---|---|---|
| [`vault-management`](./skills/vault-management/SKILL.md) | List and sync Obsidian vaults into document tables | No |
| [`knowledge-query`](./skills/knowledge-query/SKILL.md) | Query the knowledge base via semantic search (with adaptive `top_k`) | No |
| [`knowledge-ingest`](./skills/knowledge-ingest/SKILL.md) | Create/delete document tables, upload files for ingestion | No |
| [`fenix-login`](./skills/fenix-login/SKILL.md) | Log in to Fenix via browser automation | Yes |
| [`fenix-browser`](./skills/fenix-browser/SKILL.md) | Browse Fenix courses/subjects, extract content, and ingest into knowledge base | Yes |
| [`weather-fetcher`](./skills/weather-fetcher/SKILL.md) | Fetch current weather data (demo skill) | No |

### How skills work

Each `SKILL.md` has:

```yaml
---
name: skill-name
description: 'When and why to use this skill'
user-invocable: true/false
---

# Instructions in markdown

Step-by-step instructions the agent follows, including
API endpoints, shell commands, and expected outputs.
```

- **`user-invocable: true`** — The user can directly trigger this skill
- **`user-invocable: false`** — The agent uses it internally when needed (e.g. when answering a question requires querying the knowledge base)

---

## 🔧 Scripts

The [`fenix-browser`](./skills/fenix-browser/) skill includes Python and Bash scripts for browser automation:

| Script | What it does |
|---|---|
| [`get_courses.sh`](./skills/fenix-browser/scripts/get_courses.sh) | Opens Fenix academic path, takes a DOM snapshot, parses course registrations |
| [`parse_courses.py`](./skills/fenix-browser/scripts/parse_courses.py) | Parses course data from an HTML snapshot → JSON |
| [`get_subjects.sh`](./skills/fenix-browser/scripts/get_subjects.sh) | Opens a curricular plan page, parses the subjects table |
| [`parse_subjects.py`](./skills/fenix-browser/scripts/parse_subjects.py) | Parses subject data from an HTML snapshot → JSON |
| [`get_subject_page.sh`](./skills/fenix-browser/scripts/get_subject_page.sh) | Opens a subject page, extracts sidebar links and main content |
| [`parse_subject_page.py`](./skills/fenix-browser/scripts/parse_subject_page.py) | Parses subject page data from an HTML snapshot → JSON |
| [`convert_to_markdown.py`](./skills/fenix-browser/scripts/convert_to_markdown.py) | Converts a browser DOM snapshot to clean Markdown (for ingestion) |

All scripts run via `uv run python` to use the project's virtual environment. Dependencies (`beautifulsoup4`, `html-to-markdown`) are declared in this workspace's [`pyproject.toml`](./pyproject.toml).

---

## 📂 Workspace Structure

```
workspace-trivial-fenix-sinfo-2026/
├── AGENTS.md          # General agent operating instructions
├── BOOTSTRAP.md       # First-run setup (agent reads on first boot)
├── HEARTBEAT.md       # Periodic task checklist
├── IDENTITY.md        # Agent name, vibe, emoji
├── SOUL.md            # Core behavior and personality
├── TOOLS.md           # Local tool notes
├── USER.md            # Info about the human (workshop organizer)
├── pyproject.toml     # Script dependencies (beautifulsoup4, html-to-markdown)
├── resources/
│   └── avatar.png     # Agent avatar
├── skills/
│   ├── vault-management/SKILL.md
│   ├── knowledge-query/SKILL.md
│   ├── knowledge-ingest/SKILL.md
│   ├── fenix-login/SKILL.md
│   ├── fenix-browser/
│   │   ├── SKILL.md
│   │   └── scripts/   # Python + Bash automation scripts
│   └── weather-fetcher/SKILL.md
└── .openclaw/
    └── workspace-state.json
```

---

## 📦 Dependencies

This workspace has its own [`pyproject.toml`](./pyproject.toml) declaring the Python dependencies needed by its scripts:

```toml
dependencies = [
    "beautifulsoup4==4.14.0",
    "html-to-markdown==2.25.0",
]
```

All dependencies are managed from the **project root**:

```bash
# From the repo root
uv sync --all-packages
```

No extra steps needed — everything is installed in one go.

---

## 🔄 How the Agent Uses the Knowledge Service

The agent interacts with the [Knowledge Service](../knowledge_service/README.md) through three skills:

1. **`vault-management`** — Lists configured Obsidian vaults and triggers syncs to populate document tables
2. **`knowledge-query`** — Queries any document table via semantic search (`POST /document-tables/{table}/knowledge`). Adaptively adjusts `top_k` based on query complexity.
3. **`knowledge-ingest`** — Creates tables, uploads files for ingestion, and advises cleanup after use

When browsing Fenix (`fenix-browser` skill), the agent:
1. Asks the user for a table name
2. Creates the table via `knowledge-ingest`
3. Takes DOM snapshots of each page visited
4. Converts HTML → Markdown using `convert_to_markdown.py`
5. Uploads the Markdown to the table for indexing
6. After browsing, advises the user that the table can be deleted

---

[⬅️ Back to main README](../README.md)
