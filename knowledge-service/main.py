"""Defines the main application for the knowledge service."""

from datetime import datetime

from fastapi import FastAPI
from logger import setup_logger
from loguru import logger
from models.answer import KnowledgeAnswer
from models.message import Message
from models.query import KnowledgeQuery
from settings import Settings

description = """
This is the knowledge service for the Sinfo 2025 workshop.
It provides endpoints to retrieve knowledge from a knowledge base.

The service supports two main functionalities:
1. Retrieving general knowledge based on a query.
2. Retrieving knowledge from an Obsidian vault based on a query.

The knowledge answers are returned with their content and source information.
"""

settings = Settings()
setup_logger(settings)

app = FastAPI(
    title="Knowledge Service",
    description=description,
    version="1.0.0",
)


@app.get("/", summary="Welcome Message", response_model=Message)
def read_root() -> Message:
    """Root endpoint that returns a welcome message."""
    content = "Hello everyone @ Sinfo 2025!"
    timestamp = datetime.now().isoformat()
    message = Message(content=content, timestamp=timestamp)

    logger.debug("Request received at root endpoint")

    return message


@app.get("/sync/obsidian/{vault_id}", summary="Sync Obsidian Vault", response_model=Message)
def sync_obsidian(vault_id: str) -> Message:
    """Endpoint to trigger syncing of an Obsidian vault."""
    content = f"Syncing Obsidian vault with ID has been triggered: {vault_id}"
    timestamp = datetime.now().isoformat()
    message = Message(content=content, timestamp=timestamp)

    logger.debug(f"Request received to sync Obsidian vault with ID: {vault_id}")

    return message


@app.post("/knowledge", summary="Get General Knowledge", response_model=list[KnowledgeAnswer])
def get_general_knowledge(
    query: KnowledgeQuery,
) -> list[KnowledgeAnswer]:
    """Endpoint to retrieve general knowledge based on a query."""
    # Placeholder implementation
    answers: list[KnowledgeAnswer] = []

    logger.debug(f"Request received to get general knowledge with query: {query}")

    return answers


@app.post("/knowledge/obsidian/{vault_id}", summary="Get Obsidian Knowledge", response_model=list[KnowledgeAnswer])
def get_obsidian_knowledge(
    vault_id: str,
    query: KnowledgeQuery,
) -> list[KnowledgeAnswer]:
    """Endpoint to retrieve knowledge from an Obsidian vault based on a query."""
    # Placeholder implementation
    answers: list[KnowledgeAnswer] = []

    logger.debug(f"Request received to get Obsidian knowledge with query: {query} for vault ID: {vault_id}")

    return answers
