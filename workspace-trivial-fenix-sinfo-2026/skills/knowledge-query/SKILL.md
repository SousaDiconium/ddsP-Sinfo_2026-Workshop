---
name: knowledge-query
description: 'Instructions for querying knowledge from document tables via semantic search. Use this skill when the user asks questions that should be answered from the knowledge base.'
user-invocable: false
---

# Knowledge Query Skill

This skill provides instructions for querying the knowledge base. Document tables contain indexed, embedded text chunks that can be searched semantically.

## Base URL

```
http://127.0.0.1:8000
```

## Task

Answer the user's question by finding and retrieving relevant knowledge chunks from the appropriate document table, then synthesizing a clear response with cited sources.

## Instructions

### Step 1 — List Available Document Tables

Fetch the list of document tables to see what knowledge is available for querying.

- **Method:** `GET`
- **URL:** `http://127.0.0.1:8000/document-tables`
- **Headers:** `Content-Type: application/json`

Each table in the response has:
- `source` — the table name (used in the query URL)
- `document_count` — how many text chunks are indexed in this table

Tables can originate from:
- **Obsidian vault syncs** — use the `vault-management` skill to list configured vaults and understand where data came from
- **File uploads** — documents uploaded via the `knowledge-ingest` skill
- **Agent ingestion** — content the agent scraped and ingested (e.g. from Fenix browsing)

> If you need more context about which vault a table came from, invoke the `vault-management` skill to list configured vaults — vault IDs match table names.

### Step 2 — Query Knowledge

Send the user's question to the most relevant document table to retrieve matching chunks.

- **Method:** `POST`
- **URL:** `http://127.0.0.1:8000/document-tables/{tableName}/knowledge`
- **Headers:** `Content-Type: application/json`
- **Body:**
  ```json
  {
    "query": "<user's question here>"
  }
  ```

Replace `{tableName}` with the table name from Step 1 (e.g. `sinfo-generic`, `sinfo-fenix`).

The response is a JSON array of knowledge chunks. Each chunk has:
- `content` — a passage of text from the indexed documents
- `source.title` — the file path or name of the source document
- `source.link` — link to the source document
- `source.type` — the type of source (e.g. `document-table`)

### Step 3 — Synthesize and Respond

Using the retrieved knowledge chunks as context, answer the user's question in a clear, concise way.

- Combine information from multiple chunks if needed
- Always list the sources at the end of your response, using the `source.title` field (show only the filename, not the full path)
- If the chunks do not contain enough information to answer the question, say so clearly
- If no relevant table exists, suggest the user sync a vault or ingest documents first

## Expected Output Format

```
[Answer to the user's question, synthesized from the knowledge chunks]

**Sources:**
- [Filename 1]
- [Filename 2]
```

## Notes

- Always perform Step 1 (list tables) before querying, so you pick the right table
- Choose the table whose content best matches the user's question
- For general SINFO questions, prefer `sinfo-generic`; for academic/course questions, prefer `sinfo-fenix`
- Source titles may be full file paths — strip down to just the filename (e.g. `Welcome.md`) when presenting to the user
- The knowledge response may contain overlapping chunks from the same document; deduplicate sources in the output
- If the user asks to sync a vault or manage tables, delegate to the `vault-management` or `knowledge-ingest` skills respectively
