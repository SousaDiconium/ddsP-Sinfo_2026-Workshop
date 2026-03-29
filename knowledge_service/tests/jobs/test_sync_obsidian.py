import pytest
from pytest_mock import MockerFixture


@pytest.mark.anyio
async def test_sync_obsidian_vault_loads_and_processes_documents(mocker: MockerFixture) -> None:
    # given
    vault_id = "my-vault"
    mock_documents = [mocker.MagicMock(), mocker.MagicMock()]

    mock_obsidian_loader = mocker.patch("knowledge_service.jobs.sync_obsidian.obsidian_loader")
    mock_obsidian_loader.load_documents.return_value = iter(mock_documents)

    mock_ai_service = mocker.patch("knowledge_service.jobs.sync_obsidian.ai_service")

    from knowledge_service.jobs.sync_obsidian import sync_obsidian_vault

    # when
    await sync_obsidian_vault(vault_id)

    # then
    mock_obsidian_loader.load_documents.assert_called_once_with(vault_id)
    mock_ai_service.process_documents.assert_called_once_with(vault_id, mock_documents)


@pytest.mark.anyio
async def test_sync_obsidian_vault_passes_all_documents_to_ai_service(mocker: MockerFixture) -> None:
    # given
    vault_id = "vault-2"
    mock_documents = [mocker.MagicMock() for _ in range(5)]

    mock_obsidian_loader = mocker.patch("knowledge_service.jobs.sync_obsidian.obsidian_loader")
    mock_obsidian_loader.load_documents.return_value = iter(mock_documents)

    mock_ai_service = mocker.patch("knowledge_service.jobs.sync_obsidian.ai_service")

    from knowledge_service.jobs.sync_obsidian import sync_obsidian_vault

    # when
    await sync_obsidian_vault(vault_id)

    # then
    _, call_args, _ = mock_ai_service.process_documents.mock_calls[0]
    assert call_args[0] == vault_id
    assert len(call_args[1]) == 5
