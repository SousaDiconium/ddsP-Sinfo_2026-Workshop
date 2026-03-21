---
name: fenix-browser
description: 'Lists the user''s Fenix course registrations and curricular plan links using OpenClaw browser automation. Use after logging in with the fenix-login skill.'
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

## Script details

- `scripts/get_courses.sh`: Bash script for course/registration extraction
- `scripts/parse_courses.py`: Python parser for course info
- `scripts/get_subjects.sh`: Bash script for subject extraction from a curricular plan
- `scripts/parse_subjects.py`: Python parser for subject info
- `scripts/get_subject_page.sh`: Bash script for subject page extraction
- `scripts/parse_subject_page.py`: Python parser for subject page info

## Notes
- No cookies or credentials are handled by the agent — all authentication is managed by the browser profile
- If the session expires, re-run the login skill and this script
- The browser session is isolated to the `fenix` profile and persists until closed

