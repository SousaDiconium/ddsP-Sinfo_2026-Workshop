"""Defines the data model for the knowledge query in the knowledge service."""

from pydantic import BaseModel


class KnowledgeQueryDTO(BaseModel):
    """
    Represents a knowledge query.

    Attributes:
        query (str): The content of the query.

    """

    query: str
