"""DTOs for document embedding responses."""

from pydantic import BaseModel, ConfigDict


class DocumentMetaDTO(BaseModel):
    """
    DTO representing the metadata associated with a document embedding.

    Attributes:
        when: The timestamp when the document was processed or ingested.
        title: The title of the document.
        source: The source or origin of the document (e.g., file path, URL).
        split_id: An optional identifier for the split if the document was split into multiple parts.
        source_id: An optional identifier for the source of the document, used for grouping related documents together.
        page_number: An optional page number if the document represents a page from a larger source (e.g., a PDF).
        split_idx_start: An optional index indicating the starting position of the split in the original document.

    """

    when: str | None = None
    title: str | None = None
    source: str | None = None
    split_id: int | None = None
    source_id: str | None = None
    page_number: int | None = None
    split_idx_start: int | None = None


class DocumentDTO(BaseModel):
    """
    DTO representing a document embedding and its associated metadata.

    model_config: Enables ORM mode so ``from_orm`` is accepted by the pydantic plugin.

    Attributes:
        id: The unique identifier of the document embedding.
        content: The textual content of the document embedding.
        blob_mime_type: The MIME type of the original document if it was stored as a blob.
        meta: An instance of DocumentMetaDTO containing the metadata associated with the document embedding.

    """

    model_config = ConfigDict(from_attributes=True)

    id: str
    content: str
    blob_mime_type: str | None
    meta: DocumentMetaDTO

    @classmethod
    def from_orm(cls, obj: object) -> "DocumentDTO":
        """Create a DocumentDTO instance from an ORM object."""
        raw_meta: dict[str, object] = getattr(obj, "meta", {}) or {}
        return cls(
            id=obj.id,  # type: ignore[attr-defined]
            content=obj.content,  # type: ignore[attr-defined]
            blob_mime_type=obj.blob_mime_type,  # type: ignore[attr-defined]
            meta=DocumentMetaDTO(**{k: v for k, v in raw_meta.items() if k in DocumentMetaDTO.model_fields}),
        )


class PaginatedDocumentDTO(BaseModel):
    """
    DTO representing a paginated response for document embeddings.

    Attributes:
         page: The current page number (1-based).
         page_size: The number of records per page.
         total: The total number of document embeddings available for the given source.
         items: A list of DocumentDTO instances for the current page.

    """

    page: int
    page_size: int
    total: int
    items: list[DocumentDTO]
