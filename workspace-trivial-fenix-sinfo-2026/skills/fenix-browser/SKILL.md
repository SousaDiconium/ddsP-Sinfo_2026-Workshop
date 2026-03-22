---
name: fenix-browser
description: 'Lists the user''s Fenix course registrations and curricular plan links using OpenClaw browser automation, and ingests browsed content into the knowledge base. Use after logging in with the fenix-login skill.'
argument-hint: 'No argument needed — fetches the authenticated user''s course list from Fenix.'
user-invocable: true
---

# Fenix Courses Skill (OpenClaw)

# How it works

## 1. List Courses/Registrations

- **Requires login:** Run the `fenix-login` skill first to start an authenticated browser session.
- **Run the script:** Execute `bash scripts/get_courses.sh` in this skill's folder. This will:
   - Open the Fenix academic path page in the same browser session
   - Wait for the user to log in if needed
   - Take a DOM snapshot of the page
   - Parse the HTML for the "Registrations"/"Matrículas" table
   - Output a JSON list of courses with their names, degrees, years, and curricular plan URLs
- **Present results:** Display the parsed course list to the user. Offer to open curricular plan links if desired.

## 2. List Subjects from a Course

- **Select a curricular plan URL** from the course list above.
- **Run the script:** Execute `bash scripts/get_subjects.sh <curricular_plan_url>`
   - Opens the curricular plan page in the same browser session
   - Waits for the user to log in if needed
   - Takes a DOM snapshot of the page
   - Parses the HTML for the subjects table (`<table class="scplan table">`)
   - Extracts subject rows (`tr.scplandismissal`, `tr.scplanenrollment`) and their group hierarchy (`tr.scplangroup`)
   - Outputs a JSON list of subjects with their name, URL, grade, ECTS, year, semester, and group path
- **Present results:** Display the parsed subject list to the user, grouped by curricular area if desired.

## 3. Extract Subject Page & Subpages

- **Select a subject URL** from the subject list above.
- **Run the script:** Execute `bash scripts/get_subject_page.sh <subject_url>`
   - Opens the subject landing page in the same browser session
   - Waits for the user to log in if needed
   - Takes a DOM snapshot of the page
   - Parses the HTML for sidebar modules (`div.sidebar-module`) and lists all subpage links
   - Snapshots the main content (`div#content-block`)
   - Extracts all attachments (links containing `downloadFile`)
   - Outputs a JSON object with main content, sidebar subpages, and attachments
- **Present results:** Display the main content, list subpages for navigation, and offer to download attachments.

## 4. Ingesting Browsed Content

> **All information accessed during Fenix browsing should be ingested into the knowledge base** for later querying via the `knowledge-query` skill.

### Before You Start Browsing

1. **Ask the user** what table name to use for this browsing session
   - Suggest a name based on context (e.g. `fenix-fp` for the subject "Fundamentos de Programacao", `fenix-leic-a` for the LEIC-A course)
   - Let the user decide the final name
2. **Use the `knowledge-ingest` skill** to check if the table already exists and create it if not

### For HTML Page Content (Subject Pages, Subpages)

After taking a DOM snapshot of any page, convert it to markdown and ingest it:

1. **Take the snapshot:**
   ```bash
   SNAPSHOT=$(openclaw browser --browser-profile fenix snapshot --json)
   ```

2. **Convert to markdown** using the conversion script:
   ```bash
   echo "$SNAPSHOT" | uv run python scripts/convert_to_markdown.py > /tmp/fenix-page.md
   ```
   The script extracts the main content (`#content-block`) from the HTML and converts it to clean markdown using the `html-to-markdown` library.

3. **Upload the markdown file** using the `knowledge-ingest` skill:
   - Upload `/tmp/fenix-page.md` to the chosen table via `POST /document-tables/{tableName}/documents`

4. **Repeat** for each subpage you navigate to — each page snapshot should be converted and ingested.

### For Downloaded Files (PDFs, Text Documents)

When encountering attachments (files linked with `downloadFile`):

> **IMPORTANT:** Fenix download links require authentication. You **cannot** download files with a direct HTTP request (e.g. `curl` or `wget`) — it will fail with a login redirect. You **must** use the authenticated browser session to download them.

1. **Navigate to the download URL in the browser:**
   ```bash
   openclaw browser --browser-profile fenix open "<download_url>"
   ```
   This triggers the download through the authenticated session. The browser will save the file to its default downloads directory.

2. **Locate the downloaded file** in the browser's downloads folder (typically `~/Downloads/`).

3. **Upload the file** using the `knowledge-ingest` skill (`.pdf` and `.txt` files are accepted).

### After Browsing

- **Advise the user** that the table can be deleted if no longer needed
- Use the phrasing: "Would you like me to clean up the table `{tableName}` now that we're done, or keep it for later?"
- **Never delete without explicit user confirmation**

## Script details

- `scripts/get_courses.sh`: Bash script for course/registration extraction
- `scripts/parse_courses.py`: Python parser for course info
- `scripts/get_subjects.sh`: Bash script for subject extraction from a curricular plan
- `scripts/parse_subjects.py`: Python parser for subject info
- `scripts/get_subject_page.sh`: Bash script for subject page extraction
- `scripts/parse_subject_page.py`: Python parser for subject page info
- `scripts/convert_to_markdown.py`: Converts a browser JSON snapshot to clean markdown (uses `html-to-markdown` via `uv run`)

## Notes
- No cookies or credentials are handled by the agent — all authentication is managed by the browser profile
- If the session expires, re-run the login skill and this script
- The browser session is isolated to the `fenix` profile and persists until closed
- The `convert_to_markdown.py` script must be run via `uv run` from the project root to access the `html-to-markdown` dependency
- Ingestion appends to the table — browsing multiple pages builds up the knowledge base incrementally
