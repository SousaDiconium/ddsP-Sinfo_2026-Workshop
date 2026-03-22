"""Database service module for direct access to document embeddings via SQLAlchemy."""

import re

from knowledge_service.entities.document_embedding import (
    DocumentEmbeddingBase,
    document_model_factory,
)
from knowledge_service.models.document_source import DocumentSourceDTO
from knowledge_service.models.document_table import DocumentTableDTO
from knowledge_service.utils.settings import Settings
from sqlalchemy import create_engine, func, text
from sqlalchemy.orm import Session


class DatabaseService:
    """
    Service for querying document embeddings stored in a PostgreSQL/pgvector database.

    Provides paginated retrieval of raw embeddings and grouping by the
    ``source_id`` field stored inside the JSONB ``meta`` column.
    """

    _SAFE_TABLE_NAME = re.compile(r"^[A-Za-z0-9_-]+$")

    def __init__(self, settings: Settings) -> None:
        """Initialize the DatabaseService with the given settings."""
        self._engine = create_engine(settings.postgres_connection_string)

    def _validate_table_name(self, table_name: str) -> None:
        """Raise ValueError if *table_name* contains characters outside [A-Za-z0-9_-]."""
        if not self._SAFE_TABLE_NAME.match(table_name):
            raise ValueError(f"Invalid table name: {table_name!r}")

    def check_table_exists(self, table_name: str) -> bool:
        """Check if a table with the given name exists in the database."""
        self._validate_table_name(table_name)
        with self._engine.connect() as connection:
            result = connection.execute(
                text("""
                SELECT EXISTS (
                    SELECT 1
                    FROM information_schema.tables
                    WHERE table_schema = 'public' AND table_name = :table_name
                )
                """),
                {"table_name": table_name},
            )
            return bool(result.scalar())

    def create_table(self, table_name: str) -> None:
        """Create an empty document table with pgvector columns and indexes."""
        self._validate_table_name(table_name)
        if self.check_table_exists(table_name):
            raise ValueError(f"Table '{table_name}' already exists.")

        with self._engine.connect() as connection:
            connection.execute(
                text(f"""
                CREATE TABLE "{table_name}" (
                    id VARCHAR(128) PRIMARY KEY,
                    embedding VECTOR,
                    content TEXT,
                    blob_data BYTEA,
                    blob_meta JSONB,
                    blob_mime_type VARCHAR(255),
                    meta JSONB
                )
                """)  # noqa: S608
            )
            connection.commit()

    def drop_table(self, table_name: str) -> None:
        """Drop a document table and its associated indexes."""
        self._validate_table_name(table_name)
        if not self.check_table_exists(table_name):
            raise ValueError(f"Table '{table_name}' does not exist.")

        with self._engine.connect() as connection:
            connection.execute(text(f'DROP TABLE IF EXISTS "{table_name}" CASCADE'))  # noqa: S608
            connection.commit()

    def list_tables(self) -> list[DocumentTableDTO]:
        """Return a list of all table names, and their document count, in the database."""
        with self._engine.connect() as connection:
            result = connection.execute(
                text("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name
                """)
            )
            tables = [row.table_name for row in result]
            table_counts = []
            for table in tables:
                count_result = connection.execute(text(f'SELECT COUNT(*) FROM "{table}"'))  # noqa: S608 - safe since table name is returned from the database directly
                count = count_result.scalar()
                table_counts.append(DocumentTableDTO(source=table, document_count=count))
            return table_counts

    def count_document_sources(self, table_name: str) -> int:
        """Return the total number of distinct document sources in the given table."""
        self._validate_table_name(table_name)
        model = document_model_factory(table_name)

        with Session(self._engine) as session:
            total_sources = session.query(func.count(func.distinct(model.meta["source_id"].astext))).scalar()

        return int(total_sources)

    def get_document_sources_paginated(
        self,
        table_name: str,
        *,
        page: int = 1,
        page_size: int = 10,
    ) -> list[DocumentSourceDTO]:
        """
        Return a paginated list of distinct ``source_id`` values found in *table_name*.

        Args:
            table_name: Name of the pgvector table.
            page: 1-based page number.
            page_size: Number of records per page.

        Returns:
            A list of :class:`DocumentSourceDTO` instances for the requested page.

        """
        self._validate_table_name(table_name)
        model = document_model_factory(table_name)
        offset = (page - 1) * page_size

        with Session(self._engine) as session:
            rows = (
                session.query(
                    model.meta["source_id"].astext.label("source_id"),
                    model.meta["source"].astext.label("source"),
                    func.count(model.id).label("number_documents"),
                )
                .group_by(model.meta["source_id"].astext, model.meta["source"].astext)
                .order_by("source_id")
                .offset(offset)
                .limit(page_size)
                .all()
            )

        return [
            DocumentSourceDTO(
                id=row.source_id or "unknown",
                title=row.source or "unknown",
                number_documents=row.number_documents,
            )
            for row in rows
        ]

    def count_documents_for_source(self, table_name: str, source_id: str) -> int:
        """Return the total number of documents for a given *source_id*."""
        self._validate_table_name(table_name)
        model = document_model_factory(table_name)

        with Session(self._engine) as session:
            total_documents = (
                session.query(func.count(model.id)).filter(model.meta["source_id"].astext == source_id).scalar()
            )

        return int(total_documents)

    def get_documents_for_source_paginated(
        self,
        table_name: str,
        source_id: str,
        *,
        page: int = 1,
        page_size: int = 10,
    ) -> list[DocumentEmbeddingBase]:
        """
        Return a paginated list of documents for the given *source_id*.

        Args:
            table_name: Name of the pgvector table.
            source_id: Value of ``meta.source_id`` to filter by.
            page: 1-based page number.
            page_size: Number of records per page.

        Returns:
            A list of :class:`DocumentEmbeddingBase` instances for the requested page.

        """
        self._validate_table_name(table_name)
        model = document_model_factory(table_name)
        offset = (page - 1) * page_size

        with Session(self._engine) as session:
            return (
                session.query(model)
                .filter(model.meta["source_id"].astext == source_id)
                .order_by(model.id)
                .offset(offset)
                .limit(page_size)
                .all()
            )

    def get_documents_by_source_id(
        self,
        table_name: str,
        source_id: str,
    ) -> list[DocumentEmbeddingBase]:
        """
        Return all documents for the given *source_id*.

        Args:
            table_name: Name of the pgvector table.
            source_id: Value of ``meta.source_id`` to filter by.

        Returns:
            A list of :class:`DocumentEmbeddingBase` instances matching the *source_id*.

        """
        self._validate_table_name(table_name)
        model = document_model_factory(table_name)

        with Session(self._engine) as session:
            return session.query(model).filter(model.meta["source_id"].astext == source_id).order_by(model.id).all()
