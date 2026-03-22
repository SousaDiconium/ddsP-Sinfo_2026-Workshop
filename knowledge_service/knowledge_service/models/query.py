"""Defines the data model for the knowledge query in the knowledge service."""

from pydantic import BaseModel, Field


class KnowledgeQueryDTO(BaseModel):
    """
    Represents a knowledge query.

    Attributes:
        query (str): The content of the query.
        top_k (int): The number of document chunks to retrieve. Defaults to 5.

    """

    query: str
    top_k: int = Field(default=5, ge=1, le=50, description="Number of chunks to retrieve")
