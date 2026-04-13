---
name: fenix-browser
description: 'Lists the user''s Fenix course registrations and curricular plan links using OpenClaw browser automation, and ingests browsed content into the knowledge base. Use after logging in with the fenix-login skill.'
argument-hint: 'No argument needed — fetches the authenticated user''s course list from Fenix.'
user-invocable: true
---

# Fenix Courses Skill (OpenClaw)

## How it works

### Snapshot format

`openclaw browser snapshot` outputs an **accessibility tree** — an indented text representation of all interactive and semantic elements on the page. Example structure:

```
- document:
  - main:
    - heading "Title" [level=2]
    - paragraph: "Some text"
    - link "Click here":
      - /url: https://example.com
    - list:
      - listitem:
        - text: item
  - banner:
    ...
  - contentinfo:
    ...
```

The agent should read and interpret this tree directly. Annotations like `[ref=eN]`, `[checked]`, `[disabled]` are noise and can be ignored.

### General pattern for every page

1. Ensure the browser is running: `openclaw browser --browser-profile openclaw start`
2. Open the target URL: `openclaw browser --browser-profile openclaw open "<url>"`
3. Capture the accessibility tree: `TREE=$(openclaw browser --browser-profile openclaw snapshot)`
4. Parse the tree using the hints below — no script needed for extraction.

---

## 1. List Courses / Registrations

**URL:** `https://fenix.tecnico.ulisboa.pt/alumni-section/academic-path/view-curriculum`

### Tree hints

- Find a `heading` node whose text is `"Registrations"` or `"Matrículas"`
- The course rows appear **after** that heading as a series of `link` nodes (one per course)
- For each course `link` node:
  - **Course name**: the link text
  - **Plan URL**: the `/url` child of that link node
- The **degree** and **year** typically appear as `text:` nodes adjacent to each course link (same row-level indentation)

### Output

Present a list of courses with name, degree, year, and curricular plan URL. Offer to open any plan URL.

---

## 2. List Subjects from a Curricular Plan

**URL:** the `plan_url` obtained from step 1.

### Tree hints

- The curricular plan is rendered as a structured list/table
- **Group headings** appear as `heading` nodes (they label sections like "Mandatory", "Electives")
- **Subject rows** appear as `link` nodes (subject name + URL) mixed with `text:` nodes for grade, ECTS, year, semester
- For each subject `link` node:
  - **Name**: link text
  - **URL**: `/url` child
  - **ECTS / Year / Semester**: `text:` sibling nodes at the same indentation level, in order
  - **Group**: the most recent `heading` node seen before this link

### Output

Present subjects grouped by curricular area. Offer to browse individual subject pages.

---

## 3. Extract a Subject Page and Its Subpages

**URL:** the subject URL from step 2.

### Tree hints

- **Sidebar subpage links**: look for a `navigation` landmark (or `list` of `link` nodes) near the top of `main:`; these are the subpage menu entries — collect their link text and `/url`
- **Main content**: everything inside the `main:` landmark is the page content
- **Attachments / downloads**: any `link` node whose `/url` child contains `downloadFile` — collect the link text (filename) and URL

### Output

Display the main page content, list available subpages for navigation, and list any downloadable attachments.

---

## 4. Ingesting Browsed Content

> **All Fenix content accessed should be ingested into the knowledge base** for later querying via `knowledge-query`.

### Before you start browsing

1. Ask the user what table name to use for this session (e.g. `fenix-fp`, `fenix-leic-a`)
2. Use the `knowledge-ingest` skill to create the table if it does not exist yet

### For page content (subject pages, subpages)

After capturing the accessibility tree of any page, convert it to markdown and ingest:

```bash
# 1. Capture the accessibility tree
TREE=$(openclaw browser --browser-profile openclaw snapshot)

# 2. Convert to markdown (scopes to main: landmark automatically)
echo "$TREE" | uv run python scripts/convert_to_markdown.py > /tmp/fenix-page.md

# 3. Upload via knowledge-ingest skill
#    POST /document-tables/{tableName}/documents with file /tmp/fenix-page.md
```

Repeat for each subpage you navigate to.

### For downloaded files (PDFs, text documents)

> **IMPORTANT:** Fenix download links require authentication — you **cannot** use `curl`/`wget`. Use the authenticated browser session.

```bash
# Navigate to the download URL to trigger the download
openclaw browser --browser-profile openclaw open "<download_url>"
```

The browser saves the file to its default downloads directory (typically `~/Downloads/`). Then upload via the `knowledge-ingest` skill.

### After browsing

- Ask the user: *"Would you like me to clean up the table `{tableName}` now that we're done, or keep it for later?"*
- **Never delete without explicit user confirmation.**

---

## Notes

- All authentication is managed by the browser profile — no credentials are handled by the agent
- If the session expires, re-run `fenix-login` and retry
- The browser session is isolated to the `openclaw` profile and persists until closed
- `convert_to_markdown.py` must be run via `uv run` from the project root (uses the project virtual environment)
- Ingestion appends to the table — browsing multiple pages builds up the knowledge base incrementally


