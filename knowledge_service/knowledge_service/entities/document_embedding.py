"""Module defining database entities for document embeddings."""

from typing import TypedDict

from pgvector.sqlalchemy import Vector  # type: ignore[import-untyped]
from sqlalchemy import LargeBinary, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy ORM models."""

    pass


class BlobMeta(TypedDict):
    """Data class representing metadata for a binary large object (BLOB)."""

    pass


class SplitOverlapDict(TypedDict):
    """
    Data class representing the overlap information for a document split.

    Attributes:
        range (tuple[int, int]): The range of the split.
        doc_id (str): The ID of the document associated with the split.

    """

    range: tuple[int, int]
    doc_id: str


class DocumentMeta(TypedDict):
    """
    Data class representing metadata for a document.

    Attributes:
        when (str): The timestamp indicating when the document was created or modified.
        title (str): The title of the document.
        source (str): The source from which the document was obtained.
        split_id (int): The identifier for the document split.
        source_id (str): The identifier for the source of the document.
        page_number (int): The page number of the document.
        _split_overlap (list[SplitOverlapDict]): A list of overlap information for document splits.
        split_idx_start (int): The starting index of the split.

    """

    when: str
    title: str
    source: str
    split_id: int
    source_id: str
    page_number: int
    _split_overlap: list[SplitOverlapDict]
    split_idx_start: int


class DocumentEmbeddingBase(Base):
    """
    Abstract base class defining the schema for document embeddings.

    Subclass this (or use document_model_factory) to target a specific table.

    Attributes:
        id (str): The unique identifier for the document.
        embedding (Vector): The vector representation of the document.
        content (str): The textual content of the document.
        blob_data (bytes): The binary data associated with the document.
        blob_meta (dict): Metadata related to the binary data.
        blob_mime_type (str): The MIME type of the binary data.
        meta (dict): Additional metadata about the document.

    """

    __abstract__ = True

    id: Mapped[str] = mapped_column(String(128), primary_key=True, nullable=False)
    embedding: Mapped[Vector] = mapped_column(Vector)
    content: Mapped[str] = mapped_column(Text)
    blob_data: Mapped[bytes | None] = mapped_column(LargeBinary, nullable=True)
    blob_meta: Mapped[BlobMeta | None] = mapped_column(JSONB, nullable=True)
    blob_mime_type: Mapped[str | None] = mapped_column(String(255), nullable=True)
    meta: Mapped[DocumentMeta] = mapped_column(JSONB)


_model_registry: dict[str, type[DocumentEmbeddingBase]] = {}


def document_model_factory(table_name: str) -> type[DocumentEmbeddingBase]:
    """
    Return a mapped ORM class bound to the given table name.

    If the table was requested before, the cached class is returned so SQLAlchemy
    never registers two mappers for the same table.
    """
    if table_name not in _model_registry:
        _model_registry[table_name] = type(
            f"DocumentEmbedding_{table_name}",
            (DocumentEmbeddingBase,),
            {"__tablename__": table_name},
        )
    return _model_registry[table_name]
