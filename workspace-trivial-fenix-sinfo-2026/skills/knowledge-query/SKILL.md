---
name: knowledge-query
description: Instructions for querying knowledge from Obsidian vaults via the knowledge service API, and optionally syncing vaults. Use this skill when the user asks questions that should be answered from the knowledge base, or explicitly asks to sync a vault.
user-invocable: false
---

# Knowledge Query Skill

This skill provides instructions for interacting with the knowledge service to answer user questions using content stored in Obsidian vaults.

## Base URL

```
http://127.0.0.1:8000
```

## Task

Answer the user's question by fetching relevant knowledge chunks from the appropriate Obsidian vault and synthesizing a response with cited sources.

## Instructions

### Step 1 — List Available Vaults

Fetch the list of vaults to understand what knowledge is available and determine which vault best matches the user's question.

- **Method:** `GET`
- **URL:** `http://127.0.0.1:8000/obsidian-vaults`
- **Headers:** `Content-Type: application/json`

Each vault in the response has:
- `id` — used in subsequent requests (e.g. `sinfo-generic`, `sinfo-fenix`)
- `location` — path to the vault on disk
- `description` — what the vault contains; use this to decide which vault to query

**Known vaults (as of March 2026):**

| ID | Description |
|----|-------------|
| `sinfo-generic` | General information about Sinfo — the student-led tech conference at Instituto Superior Técnico. Use for questions about the event, mission, schedule, speakers, networking, etc. |
| `sinfo-fenix` | Academic information scraped from Fenix (IST's course management system). Use for questions about courses, subjects, schedules, projects, and evaluations. |

> Choose the vault whose description best matches the user's question. If uncertain, prefer `sinfo-generic` for general questions and `sinfo-fenix` for academic/course-related questions.

### Step 2 — Query Knowledge

Send the user's question to the selected vault to retrieve relevant document chunks.

- **Method:** `POST`
- **URL:** `http://127.0.0.1:8000/obsidian-vaults/{vaultId}/knowledge`
- **Headers:** `Content-Type: application/json`
- **Body:**
  ```json
  {
    "query": "<user's question here>"
  }
  ```

The response is a JSON array of knowledge chunks. Each chunk has:
- `content` — a passage of text from the vault
- `source.title` — the file path of the source document
- `source.link` — link to the source document

### Step 3 — Synthesize and Respond

Using the retrieved knowledge chunks as context, answer the user's question in a clear, concise way.

- Combine information from multiple chunks if needed
- Always list the sources at the end of your response, using the `source.title` field (show only the filename, not the full path)
- If the chunks do not contain enough information to answer the question, say so clearly

### Step 4 — Sync (ONLY when explicitly requested)

> **WARNING:** Do NOT sync automatically. Only trigger a sync if the user explicitly asks to sync a vault (e.g. "sync the vault", "refresh the knowledge base").

- **Method:** `GET`
- **URL:** `http://127.0.0.1:8000/obsidian-vaults/{vaultId}/sync`
- **Headers:** `Content-Type: application/json`

The response confirms that the sync has been triggered. After syncing, you may re-query if the user wants an updated answer.

## Expected Output Format

```
[Answer to the user's question, synthesized from the knowledge chunks]

**Sources:**
- [Filename 1]
- [Filename 2]
```

## Notes

- Always perform Step 1 (list vaults) before querying, so you understand what's available and pick the right vault
- Never trigger a sync unless the user explicitly requests it — syncing may be slow or cause side effects
- Use the `description` of each vault to route the question correctly; do not guess vault IDs
- Source titles are full file paths — strip down to just the filename (e.g. `Welcome.md`) when presenting to the user
- The knowledge response may contain overlapping chunks from the same document; deduplicate sources in the output
