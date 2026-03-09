"""
Obsidian loader module.

This module provides the ObsidianLoader class for loading and processing documents from an Obsidian vault,
including methods for syncing the vault and loading documents.
"""

from collections.abc import Generator
from pathlib import Path

import pymupdf4llm # type: ignore
from haystack import Document
from knowledge_service.utils.settings import Settings, SettingsSource
from loguru import logger


class ObsidianLoader:
    """
    Loader class for handling operations related to an Obsidian vault.

    This class provides methods to load documents from an Obsidian vault.
    """

    _settings: Settings

    def __init__(self, settings: Settings) -> None:
        """
        Initialize the ObsidianLoader with the provided settings.

        Args:
            settings (Settings): The settings object containing configuration values.

        """
        self._settings = settings

    def get_vault_config(self, vault_id: str) -> SettingsSource:
        """
        Get the configuration for the specified Obsidian vault.

        Args:
            vault_id (str): The ID of the Obsidian vault for which to retrieve the configuration.

        Returns:
            SettingsSource: The configuration source for the specified vault.

        """
        vault_config = None
        for vault in self._settings.obsidian_sources:
            if vault.id != vault_id:
                continue

            vault_config = vault
            break

        if vault_config is None:
            raise ValueError(f"Obsidian vault with ID '{vault_id}' not found in settings.")

        return vault_config

    def process_file(self, file_path: Path) -> Document | None:
        """
        Process a single file and convert it into a Document object.

        Args:
            file_path (Path): The path to the file to be processed.

        Returns:
            Optional[Document]: A Document object if the file was successfully processed,
                or None if the file type is unsupported.

        """
        extension = file_path.suffix.lower()

        # Process markdown and text files
        if extension in {".md", ".txt"}:
            with open(file_path, encoding="utf-8") as file:
                content = file.read()
                return Document(
                    content=content,
                    meta={"source": str(file_path)},
                )

        if extension in {".pdf"}:
            markdown_content = pymupdf4llm.to_markdown(file_path)
            return Document(
                content=markdown_content,
                meta={"source": str(file_path)},
            )

        logger.warning(f"Unsupported file type '{extension}' for file '{file_path}'. Skipping.")
        return None

    def load_documents(self, vault_id: str) -> Generator[Document, None, None]:
        """
        Load documents from the specified Obsidian vault.

        Args:
            vault_id (str): The ID of the Obsidian vault from which to load documents.

        Returns:
            list[Document]: A list of Document objects loaded from the vault.

        """
        source_config = self.get_vault_config(vault_id)
        vault_path = source_config.location_path

        # Iterate all files except hidden files and folders (starting with a dot)
        # and load their content as documents. The source of the document is the file path.
        for file_path in vault_path.rglob("*"):
            is_file = file_path.is_file()
            is_hidden = any(part.startswith(".") for part in file_path.parts)

            if not is_file or is_hidden:
                continue

            document = self.process_file(file_path)
            if document is not None:
                yield document
