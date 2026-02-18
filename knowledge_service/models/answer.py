"""Defines the data models for the knowledge answer in the knowledge service."""

from pydantic import BaseModel


class Source(BaseModel):
    """
    Represents the source of the knowledge answer.

    Attributes:
        type (str): The type of the source (e.g., "document", "webpage").
        title (str): The title of the source.
        link (str): The URL link to the source.

    """

    type: str
    title: str
    link: str


class KnowledgeAnswer(BaseModel):
    """
    Represents a knowledge answer.

    Attributes:
        content (str): The content of the answer.
        source (Source): The source of the answer.

    """

    content: str
    source: Source
