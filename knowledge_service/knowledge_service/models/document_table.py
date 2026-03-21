"""DTOs and models related to document tables in the knowledge service."""

from pydantic import BaseModel


class DocumentTableDTO(BaseModel):
    """
    DTO representing a document table and its associated metadata.

    Attributes:
        source: The name of the document table.
        document_count: The total number of documents in the table.

    """

    source: str
    document_count: int
