"""Module responsible for writing scraped content to markdown files with YAML front matter."""

from pathlib import Path
from typing import TextIO


def _write_metadata(file: TextIO, tags: list[str], metadata: dict[str, str]) -> None:
    """
    Write metadata as YAML front matter to the given file.

    Args:
        file (TextIO): The file object to write the metadata to.
        tags (list[str]): A list of tags to include in the YAML front matter.
        metadata (dict[str, str]): A dictionary containing metadata key-value pairs to include in the YAML front matter.

    """
    file.write("---\n")

    for key, value in metadata.items():
        file.write(f"{key}: {value}\n")
    if tags:
        file.write("tags:\n")
        for tag in tags:
            file.write(f"  - {tag}\n")

    file.write("---\n")


def write_markdown(path: Path, tags: list[str], metadata: dict[str, str], content: str) -> None:
    """
    Write content to a markdown file with YAML front matter.

    Args:
        path (Path): The path to the markdown file to write.
        tags (list[str]): A list of tags to include in the YAML front matter.
        metadata (dict[str, str]): A dictionary containing metadata key-value pairs to include in the YAML front matter.
        content (str): The markdown content to write after the front matter.

    """
    with open(path, "w", encoding="utf-8") as f:
        _write_metadata(f, tags, metadata)
        f.write(f"{content}\n")
