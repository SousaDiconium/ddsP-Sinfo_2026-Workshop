"""Job module for syncing Obsidian vaults."""

from knowledge_service import ai_service, obsidian_loader
from loguru import logger


async def sync_obsidian_vault(vault_id: str) -> None:
    """
    Sync an Obsidian vault with the given ID.

    Args:
        vault_id (str): The ID of the Obsidian vault to sync.

    """
    documents_generator = obsidian_loader.load_documents(vault_id)
    documents = list(documents_generator)
    documents_processed = ai_service.process_documents(vault_id, documents)

    logger.info(f"Synced Obsidian vault '{vault_id}' with {documents_processed} documents processed.")
    if documents_processed == 0:
        logger.warning(
            f"No documents were processed for vault '{vault_id}'. "
            "Most likely you haven't implemented the process documents pipeline completely yet."
        )
