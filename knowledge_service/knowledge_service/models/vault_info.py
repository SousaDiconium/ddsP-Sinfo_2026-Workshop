"""Defines the VaultInfoDTO model for representing information about an Obsidian vault source."""

from pydantic import BaseModel


class VaultInfoDTO(BaseModel):
    """
    Model representing the information about an Obsidian vault source.

    Attributes:
        id (str): A unique identifier for the vault.
        location (str): The file system path or URL where the vault is located.
        description (str): A brief description of the vault's contents or purpose.

    """

    id: str
    location: str
    description: str
