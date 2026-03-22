---
name: vault-management
description: 'Instructions for listing and syncing Obsidian vaults via the knowledge service API. Use this skill to see what vaults are configured and to trigger indexing of a vault into a document table.'
user-invocable: false
---

# Vault Management Skill

This skill provides instructions for managing Obsidian vault sources — listing available vaults and triggering syncs to populate document tables.

## Base URL

```
http://127.0.0.1:8000
```

## Instructions

### Step 1 — List Available Vaults

Fetch the list of configured Obsidian vaults to understand what knowledge sources are available.

- **Method:** `GET`
- **URL:** `http://127.0.0.1:8000/obsidian-vaults`
- **Headers:** `Content-Type: application/json`

Each vault in the response has:
- `id` — the vault identifier, also used as the document table name after syncing
- `location` — path to the vault on disk
- `description` — what the vault contains

**Known vaults (as of March 2026):**

| ID | Description |
|----|-------------|
| `sinfo-generic` | General information about Sinfo — the student-led tech conference at Instituto Superior Tecnico. Use for questions about the event, mission, schedule, speakers, networking, etc. |
| `sinfo-fenix` | Academic information scraped from Fenix (IST's course management system). Use for questions about courses, subjects, schedules, projects, and evaluations. |

### Step 2 — Sync a Vault (ONLY when explicitly requested)

> **WARNING:** Do NOT sync automatically. Only trigger a sync if the user explicitly asks to sync a vault (e.g. "sync the vault", "refresh the knowledge base").

Syncing reads all files in the vault, splits them into chunks, generates embeddings via Azure OpenAI, and stores them in a pgvector document table. **This rebuilds the table from scratch** — any previously indexed data in that table is replaced.

- **Method:** `GET`
- **URL:** `http://127.0.0.1:8000/obsidian-vaults/{vaultId}/sync`
- **Headers:** `Content-Type: application/json`

The response confirms the sync has been triggered. Syncing runs in the background and may take a minute depending on vault size.

## Notes

- Always list vaults (Step 1) before syncing so you pick the right vault
- Syncing **overwrites** the existing document table for that vault — all previous data is replaced
- After syncing, the vault's content is available for querying via the `knowledge-query` skill
- Use the `description` field to determine which vault is relevant; do not guess vault IDs
- If the user wants to query knowledge, use the `knowledge-query` skill instead
