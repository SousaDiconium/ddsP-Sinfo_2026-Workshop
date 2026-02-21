"""Job module for syncing Obsidian vaults."""

from knowledge_service import ai_service, obsidian_loader


async def sync_obsidian_vault(vault_id: str) -> None:
    """
    Sync an Obsidian vault with the given ID.

    Args:
        vault_id (str): The ID of the Obsidian vault to sync.

    """
    documents_generator = obsidian_loader.load_documents(vault_id)
    documents = list(documents_generator)
    ai_service.process_documents(vault_id, documents)
