"""Convert an OpenClaw browser JSON snapshot to clean markdown.

Reads a JSON snapshot from stdin (as produced by `openclaw browser snapshot --json`),
extracts the main content from the HTML (the `#content-block` div if present, otherwise
the full body), and converts it to markdown using the `html-to-markdown` library.

Usage:
    echo "$SNAPSHOT" | uv run python scripts/convert_to_markdown.py

The markdown output is printed to stdout.
"""

import json
import sys

from bs4 import BeautifulSoup
from html_to_markdown import convert as html_to_md


def main() -> None:
    """Read a JSON snapshot from stdin and print markdown to stdout."""
    try:
        snapshot = json.load(sys.stdin)
    except json.JSONDecodeError:
        print("Error: Could not parse JSON from stdin.", file=sys.stderr)
        sys.exit(1)

    html = snapshot.get("html", "")
    if not html:
        print("Error: No 'html' field found in the snapshot.", file=sys.stderr)
        sys.exit(1)

    # Try to extract just the main content block (skip nav, sidebar, footer)
    soup = BeautifulSoup(html, "html.parser")
    content_block = soup.find(id="content-block")

    if content_block:
        source_html = str(content_block)
    else:
        # Fallback to <body> or the full HTML
        body = soup.find("body")
        source_html = str(body) if body else html

    # Convert to markdown
    markdown = html_to_md(source_html)

    # Clean up excessive blank lines
    lines = markdown.splitlines()
    cleaned: list[str] = []
    prev_blank = False
    for line in lines:
        is_blank = not line.strip()
        if is_blank and prev_blank:
            continue
        cleaned.append(line)
        prev_blank = is_blank

    print("\n".join(cleaned))


if __name__ == "__main__":
    main()
