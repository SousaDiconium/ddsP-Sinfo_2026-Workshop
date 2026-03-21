#!/bin/bash
# Script to open Fenix academic path and extract course list using OpenClaw browser
# Usage: bash get_courses.sh

PROFILE=openclaw
FENIX_PATH_URL="https://fenix.tecnico.ulisboa.pt/alumni-section/academic-path/view-curriculum"

# 1. Ensure browser is running
openclaw browser --browser-profile "$PROFILE" start

# 2. Open the academic path page
echo "Opening Fenix academic path page..."
openclaw browser --browser-profile "$PROFILE" open "$FENIX_PATH_URL"

# 3. Wait for user confirmation
echo "Please log in if prompted, then press Enter to continue."
read -r _

# 4. Take a snapshot of the page
SNAPSHOT=$(openclaw browser --browser-profile "$PROFILE" snapshot --json)

# 5. Parse the HTML for course registrations (Python required)
echo "$SNAPSHOT" | python3 "$(dirname "$0")/parse_courses.py"
