"""Defines the main application for the knowledge service."""

import asyncio
import tempfile
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query, UploadFile
from loguru import logger

from knowledge_service import ai_service, db_service, obsidian_loader, settings
from knowledge_service.jobs.sync_obsidian import sync_obsidian_vault
from knowledge_service.models.answer import KnowledgeAnswerDTO, SourceDTO
from knowledge_service.models.document import (
    DocumentDTO,
    PaginatedDocumentDTO,
)
from knowledge_service.models.document_source import PaginatedDocumentSourceDTO
from knowledge_service.models.document_table import (
    CreateTableRequestDTO,
    DocumentTableDTO,
    FileUploadResponseDTO,
)
from knowledge_service.models.embedding import (
    EmbeddingCompareRequestDTO,
    EmbeddingCompareResponseDTO,
    EmbeddingRequestDTO,
    EmbeddingResponseDTO,
    EmbeddingSimilarityPairDTO,
)
from knowledge_service.models.message import MessageDTO
from knowledge_service.models.query import KnowledgeQueryDTO
from knowledge_service.models.vault_info import VaultInfoDTO

ALLOWED_EXTENSIONS = {".md", ".txt", ".pdf"}

description = """
This is the knowledge service for the Sinfo 2026 workshop.
It provides endpoints to retrieve knowledge from a knowledge base.

The service supports two main functionalities:
1. Retrieving general knowledge based on a query.
2. Retrieving knowledge from an Obsidian vault based on a query.

The knowledge answers are returned with their content and source information.
"""

app = FastAPI(
    title="Knowledge Service",
    description=description,
    version="1.0.0",
)


@app.get("/", summary="Welcome Message", response_model=MessageDTO, tags=["General"])
def read_root() -> MessageDTO:
    """Root endpoint that returns a welcome message."""
    raise HTTPException(
        status_code=501, detail="Welcome to the Knowledge Service! This endpoint is not implemented yet."
    )


# ---------------------------------------------------------------------------
# Obsidian Vaults endpoints
# ---------------------------------------------------------------------------


@app.get(
    "/obsidian-vaults", summary="List Obsidian Vaults", response_model=list[VaultInfoDTO], tags=["Obsidian Vaults"]
)
def list_obsidian_vaults() -> list[VaultInfoDTO]:
    """Endpoint to list all available Obsidian vaults."""
    logger.debug("Request received to list Obsidian vaults")

    vaults_info = [
        VaultInfoDTO(
            id=vault.id,
            location=vault.location,
            description=vault.description,
        )
        for vault in settings.obsidian_sources
    ]

    return vaults_info


@app.get(
    "/obsidian-vaults/{vault_id}/sync",
    summary="Sync Obsidian Vault",
    response_model=MessageDTO,
    tags=["Obsidian Vaults"],
)
async def sync_obsidian(vault_id: str) -> MessageDTO:
    """Endpoint to trigger syncing of an Obsidian vault."""
    logger.debug(f"Request received to sync Obsidian vault-id:{vault_id}")

    content = f"Syncing Obsidian vault with ID has been triggered: {vault_id}"
    timestamp = datetime.now().isoformat()
    message = MessageDTO(content=content, timestamp=timestamp)

    asyncio.create_task(sync_obsidian_vault(vault_id))

    return message


# ---------------------------------------------------------------------------
# Document Tables endpoints
# ---------------------------------------------------------------------------


@app.get(
    "/document-tables",
    summary="List Document Tables",
    response_model=list[DocumentTableDTO],
    tags=["Documents"],
)
def list_document_tables() -> list[DocumentTableDTO]:
    """Endpoint to list all document tables."""
    logger.debug("Request received to list document tables")
    return db_service.list_tables()


@app.get(
    "/document-tables/{table_name}/sources",
    summary="List Document Sources",
    response_model=PaginatedDocumentSourceDTO,
    tags=["Documents"],
)
def list_document_sources(
    table_name: str,
    page: int = Query(1, ge=1, description="Page number (1-based)"),
    page_size: int = Query(10, ge=1, le=100, description="Number of records per page"),
) -> PaginatedDocumentSourceDTO:
    """Endpoint to list document sources for a given table."""
    logger.debug(f"Request received to list document sources for table:{table_name} page:{page} page_size:{page_size}")

    sources = db_service.get_document_sources_paginated(table_name=table_name, page=page, page_size=page_size)
    total_sources = db_service.count_document_sources(table_name=table_name)
    return PaginatedDocumentSourceDTO(
        items=sources,
        total=total_sources,
        page=page,
        page_size=page_size,
    )


@app.get(
    "/document-tables/{table_name}/sources/{source_id}/documents",
    summary="List Documents for Source",
    response_model=PaginatedDocumentDTO,
    tags=["Documents"],
)
def list_documents_for_source(
    table_name: str,
    source_id: str,
    page: int = Query(1, ge=1, description="Page number (1-based)"),
    page_size: int = Query(10, ge=1, le=100, description="Number of records per page"),
) -> PaginatedDocumentDTO:
    """Endpoint to list documents for a given source in a specific table."""
    logger.debug(
        f"Request received to list documents for source_id:{source_id} in table:{table_name}"
        f" page:{page} page_size:{page_size}"
    )

    documents = db_service.get_documents_for_source_paginated(
        table_name=table_name,
        source_id=source_id,
        page=page,
        page_size=page_size,
    )
    total_documents = db_service.count_documents_for_source(table_name=table_name, source_id=source_id)
    return PaginatedDocumentDTO(
        items=[DocumentDTO.from_orm(doc) for doc in documents],
        total=total_documents,
        page=page,
        page_size=page_size,
    )


@app.post(
    "/document-tables",
    summary="Create Document Table",
    response_model=MessageDTO,
    tags=["Documents"],
)
def create_document_table(request: CreateTableRequestDTO) -> MessageDTO:
    """Endpoint to create an empty document table with pgvector columns and indexes."""
    logger.debug(f"Request received to create document table: {request.table_name}")

    try:
        db_service.create_table(request.table_name)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc

    return MessageDTO(
        content=f"Table '{request.table_name}' created successfully.",
        timestamp=datetime.now().isoformat(),
    )


@app.delete(
    "/document-tables/{table_name}",
    summary="Delete Document Table",
    response_model=MessageDTO,
    tags=["Documents"],
)
def delete_document_table(table_name: str) -> MessageDTO:
    """Endpoint to delete a document table and its associated indexes."""
    logger.debug(f"Request received to delete document table: {table_name}")

    try:
        db_service.drop_table(table_name)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    return MessageDTO(
        content=f"Table '{table_name}' deleted successfully.",
        timestamp=datetime.now().isoformat(),
    )


@app.post(
    "/document-tables/{table_name}/documents",
    summary="Upload Document",
    response_model=FileUploadResponseDTO,
    tags=["Documents"],
)
async def upload_document(table_name: str, file: UploadFile) -> FileUploadResponseDTO:
    """Endpoint to upload a file, process it through the ingestion pipeline, and append to a table."""
    file_name = file.filename or "unknown"
    logger.debug(f"Request received to upload document '{file_name}' to table: {table_name}")

    # Validate file extension
    extension = Path(file_name).suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        allowed = ", ".join(sorted(ALLOWED_EXTENSIONS))
        raise HTTPException(
            status_code=422,
            detail=f"Unsupported file type '{extension}'. Allowed types: {allowed}",
        )

    # Validate table exists
    if not db_service.check_table_exists(table_name):
        raise HTTPException(status_code=404, detail=f"Table '{table_name}' does not exist.")

    # Write uploaded file to a temp path so ObsidianLoader.process_file can read it
    file_content = await file.read()
    with tempfile.NamedTemporaryFile(suffix=extension, delete=False) as tmp:
        tmp.write(file_content)
        tmp_path = Path(tmp.name)

    try:
        document = obsidian_loader.process_file(tmp_path)
        if document is None:
            raise HTTPException(status_code=422, detail=f"Could not process file '{file_name}'.")

        # Override the source metadata with the original file name instead of the temp path
        document.meta["source"] = file_name

        chunks_created = ai_service.process_documents(table_name, [document], recreate_table=False)
    finally:
        tmp_path.unlink(missing_ok=True)

    return FileUploadResponseDTO(
        table_name=table_name,
        file_name=file_name,
        chunks_created=chunks_created,
        message=f"Successfully ingested '{file_name}' into table '{table_name}'.",
    )


@app.post(
    "/document-tables/{table_name}/knowledge",
    summary="Query Document Table Knowledge",
    response_model=list[KnowledgeAnswerDTO],
    tags=["Documents"],
)
def query_document_table(
    table_name: str,
    query: KnowledgeQueryDTO,
) -> list[KnowledgeAnswerDTO]:
    """Endpoint to query knowledge from a document table via semantic search."""
    logger.debug(f"Request received to query knowledge from table:{table_name} with query:{query.query}")

    if not db_service.check_table_exists(table_name):
        raise HTTPException(status_code=404, detail=f"Table '{table_name}' does not exist.")

    documents = ai_service.search_documents_table(table=table_name, query=query.query, top_k=query.top_k)
    answers = [
        KnowledgeAnswerDTO(
            content=document.content or "NO CONTENT",
            source=SourceDTO(
                title=document.meta.get("source", "Unknown Source"),
                link=document.meta.get("source", "Unknown Source"),
                type="document-table",
            ),
        )
        for document in documents
    ]

    return answers


# ---------------------------------------------------------------------------
# Embedding endpoints
# ---------------------------------------------------------------------------


@app.post(
    "/embeddings",
    summary="Generate Embedding",
    response_model=EmbeddingResponseDTO,
    tags=["Embeddings"],
)
def generate_embedding(request: EmbeddingRequestDTO) -> EmbeddingResponseDTO:
    """Endpoint to generate an embedding vector for a single text string."""
    logger.debug(f"Request received to generate embedding for text: {request.text[:80]}...")

    embedding = ai_service.embed_text(request.text)

    return EmbeddingResponseDTO(
        text=request.text,
        embedding=embedding,
        dimensions=len(embedding),
    )


@app.post(
    "/embeddings/compare",
    summary="Compare Embeddings",
    response_model=EmbeddingCompareResponseDTO,
    tags=["Embeddings"],
)
def compare_embeddings(request: EmbeddingCompareRequestDTO) -> EmbeddingCompareResponseDTO:
    """Endpoint to embed multiple texts and compute pairwise cosine similarity."""
    logger.debug(f"Request received to compare embeddings for {len(request.texts)} texts")

    embeddings_data: list[EmbeddingResponseDTO] = []
    vectors: list[list[float]] = []

    for text in request.texts:
        embedding = ai_service.embed_text(text)
        vectors.append(embedding)
        embeddings_data.append(
            EmbeddingResponseDTO(
                text=text,
                embedding=embedding,
                dimensions=len(embedding),
            )
        )

    # Compute pairwise cosine similarities
    similarities: list[EmbeddingSimilarityPairDTO] = []
    for i in range(len(request.texts)):
        for j in range(i + 1, len(request.texts)):
            dot_product = sum(a * b for a, b in zip(vectors[i], vectors[j], strict=True))
            magnitude_a = sum(a * a for a in vectors[i]) ** 0.5
            magnitude_b = sum(b * b for b in vectors[j]) ** 0.5
            cosine_sim = dot_product / (magnitude_a * magnitude_b) if magnitude_a and magnitude_b else 0.0

            similarities.append(
                EmbeddingSimilarityPairDTO(
                    text_a=request.texts[i],
                    text_b=request.texts[j],
                    similarity=round(cosine_sim, 6),
                )
            )

    return EmbeddingCompareResponseDTO(
        embeddings=embeddings_data,
        similarities=similarities,
    )
