"""Defines the main application for the knowledge service."""

import asyncio
from datetime import datetime

from fastapi import FastAPI, Query
from loguru import logger

from knowledge_service import ai_service, db_service, settings
from knowledge_service.jobs.sync_obsidian import sync_obsidian_vault
from knowledge_service.models.answer import KnowledgeAnswerDTO, SourceDTO
from knowledge_service.models.document import (
    DocumentDTO,
    PaginatedDocumentDTO,
)
from knowledge_service.models.document_source import PaginatedDocumentSourceDTO
from knowledge_service.models.document_table import DocumentTableDTO
from knowledge_service.models.message import MessageDTO
from knowledge_service.models.query import KnowledgeQueryDTO
from knowledge_service.models.vault_info import VaultInfoDTO

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
    content = "Hello everyone @ Sinfo 2026!"
    timestamp = datetime.now().isoformat()
    message = MessageDTO(content=content, timestamp=timestamp)

    logger.debug("Request received at root endpoint")

    return message


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


@app.post(
    "/obsidian-vaults/{vault_id}/knowledge",
    summary="Get Obsidian Knowledge",
    response_model=list[KnowledgeAnswerDTO],
    tags=["Obsidian Vaults"],
)
def get_obsidian_knowledge(
    vault_id: str,
    query: KnowledgeQueryDTO,
) -> list[KnowledgeAnswerDTO]:
    """Endpoint to retrieve knowledge from an Obsidian vault based on a query."""
    logger.debug(f"Request received to get Obsidian knowledge with query:{query} for vault-id:{vault_id}")

    documents = ai_service.search_documents_table(table=vault_id, query=query.query, top_k=5)
    answers = [
        KnowledgeAnswerDTO(
            content=document.content,
            source=SourceDTO(
                title=document.meta.get("source", "Unknown Source"),
                link=document.meta.get("source", "Unknown Source"),
                type="obsidian",
            ),
        )
        for document in documents
    ]

    return answers


# ---------------------------------------------------------------------------
# Document Embeddings endpoints
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
