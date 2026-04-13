"""Convert an OpenClaw browser accessibility tree snapshot to clean markdown.

Reads the accessibility tree text from stdin (as produced by `openclaw browser snapshot`),
scopes to the `main` landmark if present, and converts the tree structure to clean markdown.

Usage:
    openclaw browser --browser-profile openclaw snapshot | uv run python scripts/convert_to_markdown.py

The markdown output is printed to stdout.
"""

import re
import sys

# ARIA landmarks whose entire subtree should be skipped
_SKIP_LANDMARKS = {"banner", "contentinfo", "navigation", "dialog", "tablist", "tabpanel"}

# Regex patterns for tree elements
_RE_HEADING = re.compile(r'^heading "(.+?)"(?:\s+\[.*?\])*\s*\[level=(\d+)\]')
_RE_PARA_INLINE = re.compile(r'^paragraph:\s*"(.+)"$')
_RE_TEXT = re.compile(r'^text:\s(.+)$')
_RE_LINK = re.compile(r"^(?:link|'link) \"(.+?)\"")
_RE_URL = re.compile(r"^/url:\s*(.+)$")
_RE_STRONG = re.compile(r'^strong:\s*(.+)$')
_RE_LISTITEM = re.compile(r'^listitem[:\s]')
_RE_ANNOTATIONS = re.compile(r'\s*\[(?:ref=\w+|nth=\d+|checked|disabled|selected|level=\d+)\]')


def _indent(line: str) -> int:
    return len(line) - len(line.lstrip())


def _content(line: str) -> str:
    """Return the content after the leading '- '."""
    stripped = line.lstrip()
    return stripped[2:] if stripped.startswith("- ") else stripped


def _find_main_block(lines: list[str]) -> list[str]:
    """Return only lines inside the `main:` landmark, or all lines if not found."""
    for i, line in enumerate(lines):
        stripped = line.lstrip()
        if re.match(r"^- main[:\s]", stripped) or stripped == "- main":
            main_indent = _indent(line)
            block: list[str] = []
            for subsequent in lines[i + 1 :]:
                if subsequent.strip() and _indent(subsequent) <= main_indent:
                    break
                block.append(subsequent)
            return block
    return lines


def _should_skip_landmark(content: str) -> bool:
    for kw in _SKIP_LANDMARKS:
        if re.match(rf"^{kw}[\s:]", content) or content == kw:
            return True
    return False


def _convert(lines: list[str]) -> list[str]:
    """Walk the tree lines and emit markdown tokens."""
    result: list[str] = []
    skip_until_indent: int | None = None
    i = 0

    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue

        stripped = line.lstrip()
        if not stripped.startswith("- "):
            i += 1
            continue

        cur_indent = _indent(line)
        content = _content(line)

        # Handle active skip block
        if skip_until_indent is not None:
            if cur_indent > skip_until_indent:
                i += 1
                continue
            else:
                skip_until_indent = None

        # Skip unwanted landmarks
        if _should_skip_landmark(content):
            skip_until_indent = cur_indent
            i += 1
            continue

        # Heading
        m = _RE_HEADING.match(content)
        if m:
            text, level = m.group(1), int(m.group(2))
            result.append(f"\n{'#' * min(level, 6)} {text}\n")
            i += 1
            continue

        # Inline paragraph
        m = _RE_PARA_INLINE.match(content)
        if m:
            result.append(m.group(1))
            result.append("")
            i += 1
            continue

        # Plain text node
        m = _RE_TEXT.match(content)
        if m:
            result.append(m.group(1))
            i += 1
            continue

        # Strong/bold inline
        m = _RE_STRONG.match(content)
        if m:
            result.append(f"**{m.group(1)}**")
            i += 1
            continue

        # Link — look ahead for /url child
        m = _RE_LINK.match(content)
        if m:
            link_text = m.group(1)
            url: str | None = None
            j = i + 1
            while j < len(lines):
                next_line = lines[j]
                if not next_line.strip():
                    j += 1
                    continue
                if _indent(next_line) <= cur_indent:
                    break
                nc = _content(next_line)
                url_m = _RE_URL.match(nc)
                if url_m:
                    url = url_m.group(1).strip()
                    break
                j += 1
            if url:
                result.append(f"[{link_text}]({url})")
            else:
                result.append(link_text)
            i += 1
            continue

        # List item — just a structural container; children will be picked up
        if _RE_LISTITEM.match(content):
            result.append("")  # visual separation between items
            i += 1
            continue

        # Containers (document, list, group, main, section, article, …) — traverse into them
        i += 1

    return result


def main() -> None:
    """Read an accessibility tree from stdin and print markdown to stdout."""
    raw = sys.stdin.read()
    if not raw.strip():
        print("Error: No input received on stdin.", file=sys.stderr)
        sys.exit(1)

    lines = raw.splitlines()
    main_lines = _find_main_block(lines)
    tokens = _convert(main_lines)

    markdown = "\n".join(tokens)

    # Collapse runs of 3+ blank lines into 2
    markdown = re.sub(r"\n{3,}", "\n\n", markdown)

    print(markdown.strip())


if __name__ == "__main__":
    main()

