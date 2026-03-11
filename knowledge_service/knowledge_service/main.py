"""Defines the main application for the knowledge service."""

import asyncio
from datetime import datetime

from fastapi import FastAPI
from loguru import logger

from knowledge_service import ai_service
from knowledge_service.jobs.sync_obsidian import sync_obsidian_vault
from knowledge_service.models.answer import KnowledgeAnswer, Source
from knowledge_service.models.message import Message
from knowledge_service.models.query import KnowledgeQuery

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


@app.get("/", summary="Welcome Message", response_model=Message)
def read_root() -> Message:
    """Root endpoint that returns a welcome message."""
    content = "Hello everyone @ Sinfo 2026!"
    timestamp = datetime.now().isoformat()
    message = Message(content=content, timestamp=timestamp)

    logger.debug("Request received at root endpoint")

    return message


@app.get("/sync/obsidian/{vault_id}", summary="Sync Obsidian Vault", response_model=Message)
async def sync_obsidian(vault_id: str) -> Message:
    """Endpoint to trigger syncing of an Obsidian vault."""
    content = f"Syncing Obsidian vault with ID has been triggered: {vault_id}"
    timestamp = datetime.now().isoformat()
    message = Message(content=content, timestamp=timestamp)

    logger.debug(f"Request received to sync Obsidian vault with ID: {vault_id}")
    asyncio.create_task(sync_obsidian_vault(vault_id))

    return message


@app.post("/knowledge", summary="Get General Knowledge", response_model=list[KnowledgeAnswer])
def get_general_knowledge(
    query: KnowledgeQuery,
) -> list[KnowledgeAnswer]:
    """Endpoint to retrieve general knowledge based on a query."""
    # Placeholder implementation
    answers: list[KnowledgeAnswer] = []

    logger.debug(f"Request received to get general knowledge with query: {query}")

    documents = ai_service.search_documents_database(query=query.query, top_k=5)
    answers = [
        KnowledgeAnswer(
            content=document.content,
            source=Source(
                title=document.meta.get("source", "Unknown Source"),
                link=document.meta.get("source", "Unknown Source"),
                type=document.meta.get("type", "unknown"),
            ),
        )
        for document in documents
    ]

    return answers


@app.post("/knowledge/obsidian/{vault_id}", summary="Get Obsidian Knowledge", response_model=list[KnowledgeAnswer])
def get_obsidian_knowledge(
    vault_id: str,
    query: KnowledgeQuery,
) -> list[KnowledgeAnswer]:
    """Endpoint to retrieve knowledge from an Obsidian vault based on a query."""
    logger.debug(f"Request received to get Obsidian knowledge with query: {query} for vault ID: {vault_id}")

    documents = ai_service.search_documents_table(table=vault_id, query=query.query, top_k=5)
    answers = [
        KnowledgeAnswer(
            content=document.content,
            source=Source(
                title=document.meta.get("source", "Unknown Source"),
                link=document.meta.get("source", "Unknown Source"),
                type="obsidian",
            ),
        )
        for document in documents
    ]

    return answers
