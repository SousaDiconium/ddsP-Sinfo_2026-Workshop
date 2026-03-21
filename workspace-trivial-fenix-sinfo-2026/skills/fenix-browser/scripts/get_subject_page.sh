#!/bin/bash
# Script to open a Fenix subject page and extract sidebar subpages using OpenClaw browser
# Usage: bash get_subject_page.sh <subject_url>

PROFILE=openclaw
SUBJECT_URL="$1"

if [ -z "$SUBJECT_URL" ]; then
  echo "Usage: bash get_subject_page.sh <subject_url>"
  exit 1
fi

# 1. Ensure browser is running
openclaw browser --browser-profile "$PROFILE" start

# 2. Open the subject landing page
echo "Opening Fenix subject page..."
openclaw browser --browser-profile "$PROFILE" open "$SUBJECT_URL"

# 3. Wait for user confirmation
echo "Please log in if prompted, then press Enter to continue."
read -r _

# 4. Take a snapshot of the page
SNAPSHOT=$(openclaw browser --browser-profile "$PROFILE" snapshot --json)

# 5. Parse the HTML for sidebar subpages (Python required)
echo "$SNAPSHOT" | python3 "$(dirname "$0")/parse_subject_page.py"
