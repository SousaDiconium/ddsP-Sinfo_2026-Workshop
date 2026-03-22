---
name: knowledge-ingest
description: 'Instructions for creating document tables, uploading files for ingestion, and deleting tables. Use this skill when the agent or user needs to store new knowledge in the database, or manage existing tables.'
user-invocable: false
---

# Knowledge Ingest Skill

This skill provides instructions for managing document tables and ingesting new content into the knowledge base. Use it when you need to store information for later querying.

## Base URL

```
http://127.0.0.1:8000
```

## Instructions

### List Existing Tables

Before creating or deleting, check what already exists.

- **Method:** `GET`
- **URL:** `http://127.0.0.1:8000/document-tables`
- **Headers:** `Content-Type: application/json`

### Create a Document Table

Create an empty table to ingest documents into.

- **Method:** `POST`
- **URL:** `http://127.0.0.1:8000/document-tables`
- **Headers:** `Content-Type: application/json`
- **Body:**
  ```json
  {
    "table_name": "<desired-table-name>"
  }
  ```

**Table naming guidelines:**
- Use lowercase with hyphens (e.g. `fenix-fp`, `sinfo-speakers`, `my-notes`)
- **Always ask the user** what name to use before creating — suggest a name based on context but let them decide
- Check if the table already exists first to avoid errors (409 Conflict)

### Upload a Document for Ingestion

Upload a file to be chunked, embedded, and appended to an existing table.

- **Method:** `POST`
- **URL:** `http://127.0.0.1:8000/document-tables/{tableName}/documents`
- **Content-Type:** `multipart/form-data`
- **Body:** file upload (field name: `file`)

**Accepted file formats:** `.md`, `.txt`, `.pdf`

The server will:
1. Validate the file type
2. Split the content into ~100-word chunks with 30-word overlap
3. Generate embedding vectors for each chunk via Azure OpenAI
4. Append the chunks to the specified table (existing data is preserved)

The response includes:
- `chunks_created` — number of text chunks generated and stored
- `file_name` — the original filename
- `message` — status message

### Delete a Document Table

Drop a table and all its indexed data. **This is irreversible.**

- **Method:** `DELETE`
- **URL:** `http://127.0.0.1:8000/document-tables/{tableName}`
- **Headers:** `Content-Type: application/json`

> **IMPORTANT — Deletion Policy:**
> - After a task or browsing session is complete, **always advise the user** that temporary tables can be cleaned up to save space
> - **Never delete a table without explicit user confirmation** — always ask first
> - Phrase it as a suggestion: "Would you like me to clean up the table `{tableName}` now that we're done, or keep it for later?"
> - If the user says no or doesn't respond, leave the table in place

## Typical Workflows

### Agent browsing and ingesting
1. Ask the user for a table name (suggest one based on context)
2. Create the table
3. As you browse/scrape content, convert to markdown and upload files
4. When done, advise the user the table can be deleted

### User uploading documents
1. Check if the target table exists; create if not
2. Upload the file(s)
3. Confirm the number of chunks created

## Notes

- Uploading **appends** to existing data — it never wipes the table
- To rebuild a table from scratch, delete it first, then recreate and re-upload
- Vault syncs (via the `vault-management` skill) also create/rebuild tables, but they **overwrite** all existing data in that table
- Use the `knowledge-query` skill to query the ingested content after upload
