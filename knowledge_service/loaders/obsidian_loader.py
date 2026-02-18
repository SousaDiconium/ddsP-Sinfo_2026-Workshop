"""
Obsidian loader module.

This module provides the ObsidianLoader class for loading and processing documents from an Obsidian vault,
including methods for syncing the vault and loading documents.
"""

from collections.abc import Generator
from pathlib import Path

from haystack import Document
from knowledge_service.settings import Settings, SettingsSource


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

    def load_documents(self, vault_id: str) -> Generator[Document, None, None]:
        """
        Load documents from the specified Obsidian vault.

        Args:
            vault_id (str): The ID of the Obsidian vault from which to load documents.

        Returns:
            list[Document]: A list of Document objects loaded from the vault.

        """
        source_config = self.get_vault_config(vault_id)
        vault_path = Path(source_config.location)

        # Iterate all files except hidden files and folders (starting with a dot)
        # and load their content as documents. The source of the document is the file path.
        for file_path in vault_path.rglob("*"):
            is_file = file_path.is_file()
            is_hidden = any(part.startswith(".") for part in file_path.parts)

            if not is_file or is_hidden:
                continue

            with open(file_path, encoding="utf-8") as file:
                content = file.read()
                yield Document(
                    content=content,
                    meta={"source": str(file_path)},
                )
