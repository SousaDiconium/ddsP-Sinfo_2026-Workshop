"""DTOs for document embedding source responses."""

from pydantic import BaseModel


class DocumentSourceDTO(BaseModel):
    """
    DTO representing a document source and its associated metadata.

    Attributes:
        id: The unique identifier of the document source.
        title: The title or name of the document source.
        number_documents: The total number of documents associated with this source.

    """

    id: str
    title: str
    number_documents: int


class PaginatedDocumentSourceDTO(BaseModel):
    """
    DTO representing a paginated response for document sources.

    Attributes:
        page: The current page number (1-based).
        page_size: The number of records per page.
        total: The total number of document sources available.
        items: A list of DocumentSourceDTO instances for the current page.

    """

    page: int
    page_size: int
    total: int
    items: list[DocumentSourceDTO]
