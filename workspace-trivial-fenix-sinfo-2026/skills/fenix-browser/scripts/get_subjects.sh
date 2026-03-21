#!/bin/bash
# Script to open a Fenix curricular plan page and extract subjects using OpenClaw browser
# Usage: bash get_subjects.sh <curricular_plan_url>

PROFILE=openclaw
PLAN_URL="$1"

if [ -z "$PLAN_URL" ]; then
  echo "Usage: bash get_subjects.sh <curricular_plan_url>"
  exit 1
fi

# 1. Ensure browser is running
openclaw browser --browser-profile "$PROFILE" start

# 2. Open the curricular plan page
echo "Opening Fenix curricular plan page..."
openclaw browser --browser-profile "$PROFILE" open "$PLAN_URL"

# 3. Wait for user confirmation
echo "Please log in if prompted, then press Enter to continue."
read -r _

# 4. Take a snapshot of the page
SNAPSHOT=$(openclaw browser --browser-profile "$PROFILE" snapshot --json)

# 5. Parse the HTML for subjects (Python required)
echo "$SNAPSHOT" | python3 "$(dirname "$0")/parse_subjects.py"
