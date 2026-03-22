"""API client for the knowledge service backend."""

from typing import Any, cast

import requests

BASE_URL = "http://127.0.0.1:8000"


def _get(path: str, params: dict[str, Any] | None = None) -> Any:  # noqa: ANN401
    """Perform a GET request to the API."""
    resp = requests.get(f"{BASE_URL}{path}", params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def _post(path: str, json: dict[str, Any] | None = None) -> Any:  # noqa: ANN401
    """Perform a POST request to the API."""
    resp = requests.post(f"{BASE_URL}{path}", json=json, timeout=60)
    resp.raise_for_status()
    return resp.json()


# -- General ------------------------------------------------------------------


def get_welcome() -> dict[str, Any]:
    """Fetch the welcome message (health check)."""
    return cast(dict[str, Any], _get("/"))


# -- Obsidian Vaults ----------------------------------------------------------


def list_vaults() -> list[dict[str, Any]]:
    """List all configured Obsidian vaults."""
    return cast(list[dict[str, Any]], _get("/obsidian-vaults"))


def sync_vault(vault_id: str) -> dict[str, Any]:
    """Trigger syncing of an Obsidian vault."""
    return cast(dict[str, Any], _get(f"/obsidian-vaults/{vault_id}/sync"))


def query_vault(vault_id: str, query: str) -> list[dict[str, Any]]:
    """Query knowledge from an Obsidian vault."""
    return cast(
        list[dict[str, Any]],
        _post(f"/obsidian-vaults/{vault_id}/knowledge", json={"query": query}),
    )


# -- Documents ----------------------------------------------------------------


def list_document_tables() -> list[dict[str, Any]]:
    """List all document tables."""
    return cast(list[dict[str, Any]], _get("/document-tables"))


def list_document_sources(
    table_name: str,
    page: int = 1,
    page_size: int = 10,
) -> dict[str, Any]:
    """List sources in a document table."""
    return cast(
        dict[str, Any],
        _get(
            f"/document-tables/{table_name}/sources",
            params={"page": page, "page_size": page_size},
        ),
    )


def list_documents_for_source(
    table_name: str,
    source_id: str,
    page: int = 1,
    page_size: int = 10,
) -> dict[str, Any]:
    """List document chunks for a specific source."""
    return cast(
        dict[str, Any],
        _get(
            f"/document-tables/{table_name}/sources/{source_id}/documents",
            params={"page": page, "page_size": page_size},
        ),
    )


# -- Embeddings ---------------------------------------------------------------


def generate_embedding(text: str) -> dict[str, Any]:
    """Generate an embedding vector for a single text."""
    return cast(dict[str, Any], _post("/embeddings", json={"text": text}))


def compare_embeddings(texts: list[str]) -> dict[str, Any]:
    """Compare embeddings of multiple texts."""
    return cast(
        dict[str, Any],
        _post("/embeddings/compare", json={"texts": texts}),
    )
