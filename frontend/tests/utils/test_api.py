from typing import Any

from frontend.utils.api import (
    BASE_URL,
    _delete,
    _get,
    _post,
    _post_file,
    compare_embeddings,
    create_table,
    delete_table,
    generate_embedding,
    get_welcome,
    list_document_sources,
    list_document_tables,
    list_documents_for_source,
    list_vaults,
    query_table,
    sync_vault,
    upload_document,
)
from pytest_mock import MockerFixture

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_response_mock(mocker: MockerFixture, return_value: Any) -> Any:
    mock_resp = mocker.MagicMock()
    mock_resp.raise_for_status = mocker.Mock()
    mock_resp.json.return_value = return_value
    return mock_resp


# ---------------------------------------------------------------------------
# Private HTTP helpers
# ---------------------------------------------------------------------------


class TestGetHelper:
    def test_calls_requests_get_with_full_url(self, mocker: MockerFixture) -> None:
        # given
        mock_resp = _make_response_mock(mocker, {"key": "value"})
        mock_get = mocker.patch("frontend.utils.api.requests.get", return_value=mock_resp)

        # when
        _get("/some/path")

        # then
        mock_get.assert_called_once_with(f"{BASE_URL}/some/path", params=None, timeout=30)

    def test_passes_params(self, mocker: MockerFixture) -> None:
        # given
        mock_resp = _make_response_mock(mocker, {})
        mock_get = mocker.patch("frontend.utils.api.requests.get", return_value=mock_resp)

        # when
        _get("/path", params={"page": 1, "page_size": 10})

        # then
        _, kwargs = mock_get.call_args
        assert kwargs["params"] == {"page": 1, "page_size": 10}

    def test_calls_raise_for_status(self, mocker: MockerFixture) -> None:
        # given
        mock_resp = _make_response_mock(mocker, {})
        mocker.patch("frontend.utils.api.requests.get", return_value=mock_resp)

        # when
        _get("/path")

        # then
        mock_resp.raise_for_status.assert_called_once()

    def test_returns_json_body(self, mocker: MockerFixture) -> None:
        # given
        mock_resp = _make_response_mock(mocker, {"content": "hello"})
        mocker.patch("frontend.utils.api.requests.get", return_value=mock_resp)

        # when
        result = _get("/path")

        # then
        assert result == {"content": "hello"}


class TestPostHelper:
    def test_calls_requests_post_with_full_url(self, mocker: MockerFixture) -> None:
        # given
        mock_resp = _make_response_mock(mocker, {})
        mock_post = mocker.patch("frontend.utils.api.requests.post", return_value=mock_resp)

        # when
        _post("/submit")

        # then
        mock_post.assert_called_once_with(f"{BASE_URL}/submit", json=None, timeout=60)

    def test_passes_json_body(self, mocker: MockerFixture) -> None:
        # given
        mock_resp = _make_response_mock(mocker, {})
        mock_post = mocker.patch("frontend.utils.api.requests.post", return_value=mock_resp)

        # when
        _post("/submit", json={"query": "test"})

        # then
        _, kwargs = mock_post.call_args
        assert kwargs["json"] == {"query": "test"}

    def test_calls_raise_for_status(self, mocker: MockerFixture) -> None:
        # given
        mock_resp = _make_response_mock(mocker, {})
        mocker.patch("frontend.utils.api.requests.post", return_value=mock_resp)

        # when
        _post("/submit")

        # then
        mock_resp.raise_for_status.assert_called_once()

    def test_returns_json_body(self, mocker: MockerFixture) -> None:
        # given
        mock_resp = _make_response_mock(mocker, {"id": "new-id"})
        mocker.patch("frontend.utils.api.requests.post", return_value=mock_resp)

        # when
        result = _post("/submit")

        # then
        assert result == {"id": "new-id"}


class TestDeleteHelper:
    def test_calls_requests_delete_with_full_url(self, mocker: MockerFixture) -> None:
        # given
        mock_resp = _make_response_mock(mocker, {})
        mock_delete = mocker.patch("frontend.utils.api.requests.delete", return_value=mock_resp)

        # when
        _delete("/resource/1")

        # then
        mock_delete.assert_called_once_with(f"{BASE_URL}/resource/1", timeout=30)

    def test_calls_raise_for_status(self, mocker: MockerFixture) -> None:
        # given
        mock_resp = _make_response_mock(mocker, {})
        mocker.patch("frontend.utils.api.requests.delete", return_value=mock_resp)

        # when
        _delete("/resource/1")

        # then
        mock_resp.raise_for_status.assert_called_once()

    def test_returns_json_body(self, mocker: MockerFixture) -> None:
        # given
        mock_resp = _make_response_mock(mocker, {"deleted": True})
        mocker.patch("frontend.utils.api.requests.delete", return_value=mock_resp)

        # when
        result = _delete("/resource/1")

        # then
        assert result == {"deleted": True}


class TestPostFileHelper:
    def test_calls_requests_post_with_files_dict(self, mocker: MockerFixture) -> None:
        # given
        mock_resp = _make_response_mock(mocker, {})
        mock_post = mocker.patch("frontend.utils.api.requests.post", return_value=mock_resp)
        file_bytes = b"fake file content"

        # when
        _post_file("/upload", file_bytes, "doc.md")

        # then
        mock_post.assert_called_once_with(
            f"{BASE_URL}/upload",
            files={"file": ("doc.md", file_bytes)},
            timeout=120,
        )

    def test_calls_raise_for_status(self, mocker: MockerFixture) -> None:
        # given
        mock_resp = _make_response_mock(mocker, {})
        mocker.patch("frontend.utils.api.requests.post", return_value=mock_resp)

        # when
        _post_file("/upload", b"data", "file.txt")

        # then
        mock_resp.raise_for_status.assert_called_once()

    def test_returns_json_body(self, mocker: MockerFixture) -> None:
        # given
        mock_resp = _make_response_mock(mocker, {"chunks_created": 3})
        mocker.patch("frontend.utils.api.requests.post", return_value=mock_resp)

        # when
        result = _post_file("/upload", b"data", "file.txt")

        # then
        assert result == {"chunks_created": 3}


# ---------------------------------------------------------------------------
# Public API functions
# ---------------------------------------------------------------------------


class TestGetWelcome:
    def test_calls_get_on_root(self, mocker: MockerFixture) -> None:
        # given
        mock_get = mocker.patch("frontend.utils.api._get", return_value={"content": "hello"})

        # when
        result = get_welcome()

        # then
        mock_get.assert_called_once_with("/")
        assert result == {"content": "hello"}


class TestListVaults:
    def test_calls_get_obsidian_vaults(self, mocker: MockerFixture) -> None:
        # given
        mock_get = mocker.patch("frontend.utils.api._get", return_value=[{"id": "vault-1"}])

        # when
        result = list_vaults()

        # then
        mock_get.assert_called_once_with("/obsidian-vaults")
        assert result == [{"id": "vault-1"}]


class TestSyncVault:
    def test_calls_get_with_vault_id(self, mocker: MockerFixture) -> None:
        # given
        mock_get = mocker.patch("frontend.utils.api._get", return_value={"content": "syncing"})

        # when
        result = sync_vault("my-vault")

        # then
        mock_get.assert_called_once_with("/obsidian-vaults/my-vault/sync")
        assert result == {"content": "syncing"}


class TestListDocumentTables:
    def test_calls_get_document_tables(self, mocker: MockerFixture) -> None:
        # given
        mock_get = mocker.patch("frontend.utils.api._get", return_value=[{"source": "table_1"}])

        # when
        result = list_document_tables()

        # then
        mock_get.assert_called_once_with("/document-tables")
        assert result == [{"source": "table_1"}]


class TestCreateTable:
    def test_calls_post_with_table_name(self, mocker: MockerFixture) -> None:
        # given
        mock_post = mocker.patch("frontend.utils.api._post", return_value={"content": "created"})

        # when
        result = create_table("my_table")

        # then
        mock_post.assert_called_once_with("/document-tables", json={"table_name": "my_table"})
        assert result == {"content": "created"}


class TestDeleteTable:
    def test_calls_delete_with_table_name(self, mocker: MockerFixture) -> None:
        # given
        mock_delete = mocker.patch("frontend.utils.api._delete", return_value={"content": "deleted"})

        # when
        result = delete_table("my_table")

        # then
        mock_delete.assert_called_once_with("/document-tables/my_table")
        assert result == {"content": "deleted"}


class TestUploadDocument:
    def test_calls_post_file_with_correct_args(self, mocker: MockerFixture) -> None:
        # given
        mock_post_file = mocker.patch("frontend.utils.api._post_file", return_value={"chunks_created": 5})
        file_bytes = b"file content"

        # when
        result = upload_document("my_table", file_bytes, "note.md")

        # then
        mock_post_file.assert_called_once_with("/document-tables/my_table/documents", file_bytes, "note.md")
        assert result == {"chunks_created": 5}


class TestQueryTable:
    def test_calls_post_with_correct_json(self, mocker: MockerFixture) -> None:
        # given
        mock_post = mocker.patch("frontend.utils.api._post", return_value=[{"content": "answer"}])

        # when
        result = query_table("my_table", "What is RAG?", top_k=3)

        # then
        mock_post.assert_called_once_with(
            "/document-tables/my_table/knowledge",
            json={"query": "What is RAG?", "top_k": 3},
        )
        assert result == [{"content": "answer"}]

    def test_default_top_k_is_5(self, mocker: MockerFixture) -> None:
        # given
        mock_post = mocker.patch("frontend.utils.api._post", return_value=[])

        # when
        query_table("my_table", "query")

        # then
        _, kwargs = mock_post.call_args
        assert kwargs["json"]["top_k"] == 5


class TestListDocumentSources:
    def test_calls_get_with_pagination_params(self, mocker: MockerFixture) -> None:
        # given
        mock_get = mocker.patch("frontend.utils.api._get", return_value={"items": [], "total": 0})

        # when
        result = list_document_sources("my_table", page=2, page_size=20)

        # then
        mock_get.assert_called_once_with(
            "/document-tables/my_table/sources",
            params={"page": 2, "page_size": 20},
        )
        assert result == {"items": [], "total": 0}

    def test_default_pagination(self, mocker: MockerFixture) -> None:
        # given
        mock_get = mocker.patch("frontend.utils.api._get", return_value={})

        # when
        list_document_sources("my_table")

        # then
        _, kwargs = mock_get.call_args
        assert kwargs["params"] == {"page": 1, "page_size": 10}


class TestListDocumentsForSource:
    def test_calls_get_with_source_id_and_params(self, mocker: MockerFixture) -> None:
        # given
        mock_get = mocker.patch("frontend.utils.api._get", return_value={"items": []})

        # when
        result = list_documents_for_source("my_table", "src-1", page=1, page_size=5)

        # then
        mock_get.assert_called_once_with(
            "/document-tables/my_table/sources/src-1/documents",
            params={"page": 1, "page_size": 5},
        )
        assert result == {"items": []}


class TestGenerateEmbedding:
    def test_calls_post_with_text(self, mocker: MockerFixture) -> None:
        # given
        mock_post = mocker.patch("frontend.utils.api._post", return_value={"embedding": [0.1, 0.2]})

        # when
        result = generate_embedding("hello world")

        # then
        mock_post.assert_called_once_with("/embeddings", json={"text": "hello world"})
        assert result == {"embedding": [0.1, 0.2]}


class TestCompareEmbeddings:
    def test_calls_post_with_texts_list(self, mocker: MockerFixture) -> None:
        # given
        mock_post = mocker.patch("frontend.utils.api._post", return_value={"similarities": []})

        # when
        result = compare_embeddings(["text a", "text b"])

        # then
        mock_post.assert_called_once_with("/embeddings/compare", json={"texts": ["text a", "text b"]})
        assert result == {"similarities": []}
