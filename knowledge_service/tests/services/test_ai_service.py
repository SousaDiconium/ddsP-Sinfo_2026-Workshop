from typing import cast

import pytest
from haystack import Document
from haystack.components.preprocessors import DocumentSplitter
from knowledge_service.services.ai_service import AIService
from knowledge_service.utils.settings import Settings
from pytest_mock import MockerFixture


@pytest.fixture
def mock_settings(mocker: MockerFixture) -> Settings:
    settings = mocker.MagicMock(spec=Settings)
    settings.postgres_connection_string = "postgresql://test:test@localhost/test"
    settings.azure_openai_embeddings_api_key = "test-key"
    settings.azure_openai_embeddings_api_version = "2024-01-01"
    settings.azure_openai_embeddings_endpoint = "https://test.openai.azure.com"
    settings.azure_openai_embeddings_deployment_name = "text-embedding-ada-002"
    settings.azure_openai_embeddings_embedding_dimension = 1536
    settings.obsidian_sources = []
    return cast(Settings, settings)


@pytest.fixture
def ai_service(mock_settings: Settings) -> AIService:
    return AIService(mock_settings)


class TestAIServiceInit:
    def test_stores_settings(self, mocker: MockerFixture) -> None:
        # given
        mock_settings = mocker.MagicMock(spec=Settings)

        # when
        service = AIService(mock_settings)

        # then
        assert service._settings is mock_settings

    def test_initializes_empty_document_stores(self, mocker: MockerFixture) -> None:
        # given
        mock_settings = mocker.MagicMock(spec=Settings)

        # when
        service = AIService(mock_settings)

        # then
        assert service._document_stores == {}


class TestAddDocumentStore:
    def test_creates_and_returns_store(self, ai_service: AIService, mocker: MockerFixture) -> None:
        # given
        mock_store = mocker.MagicMock()
        mocker.patch("knowledge_service.services.ai_service.PgvectorDocumentStore", return_value=mock_store)

        # when
        result = ai_service.add_document_store("my_table")

        # then
        assert result is mock_store

    def test_caches_store_by_table_name(self, ai_service: AIService, mocker: MockerFixture) -> None:
        # given
        mock_store = mocker.MagicMock()
        mocker.patch("knowledge_service.services.ai_service.PgvectorDocumentStore", return_value=mock_store)

        # when
        ai_service.add_document_store("cached_table")

        # then
        assert ai_service._document_stores["cached_table"] is mock_store

    def test_passes_recreate_table_flag(self, ai_service: AIService, mocker: MockerFixture) -> None:
        # given
        mock_store_cls = mocker.patch("knowledge_service.services.ai_service.PgvectorDocumentStore")

        # when
        ai_service.add_document_store("my_table", recreate_table=True)

        # then
        _, kwargs = mock_store_cls.call_args
        assert kwargs["recreate_table"] is True


class TestGetDocumentSplitter:
    def test_returns_document_splitter(self, ai_service: AIService) -> None:
        # when
        splitter = ai_service.get_document_splitter()

        # then
        assert isinstance(splitter, DocumentSplitter)

    def test_splitter_configured_by_word(self, ai_service: AIService) -> None:
        # when
        splitter = ai_service.get_document_splitter()

        # then
        assert splitter.split_by == "word"

    def test_splitter_split_length(self, ai_service: AIService) -> None:
        # when
        splitter = ai_service.get_document_splitter()

        # then
        assert splitter.split_length == 100

    def test_splitter_split_overlap(self, ai_service: AIService) -> None:
        # when
        splitter = ai_service.get_document_splitter()

        # then
        assert splitter.split_overlap == 30


class TestGetDocumentEmbedder:
    def test_returns_embedder_with_correct_config(self, ai_service: AIService, mocker: MockerFixture) -> None:
        # given
        mock_embedder = mocker.MagicMock()
        mock_cls = mocker.patch(
            "knowledge_service.services.ai_service.AzureOpenAIDocumentEmbedder", return_value=mock_embedder
        )

        # when
        result = ai_service.get_document_embedder()

        # then
        assert result is mock_embedder
        _, kwargs = mock_cls.call_args
        assert kwargs["api_version"] == "2024-01-01"
        assert kwargs["azure_endpoint"] == "https://test.openai.azure.com"
        assert kwargs["azure_deployment"] == "text-embedding-ada-002"


class TestGetTextEmbedder:
    def test_returns_embedder_with_correct_config(self, ai_service: AIService, mocker: MockerFixture) -> None:
        # given
        mock_embedder = mocker.MagicMock()
        mock_cls = mocker.patch(
            "knowledge_service.services.ai_service.AzureOpenAITextEmbedder", return_value=mock_embedder
        )

        # when
        result = ai_service.get_text_embedder()

        # then
        assert result is mock_embedder
        _, kwargs = mock_cls.call_args
        assert kwargs["api_version"] == "2024-01-01"
        assert kwargs["azure_endpoint"] == "https://test.openai.azure.com"
        assert kwargs["azure_deployment"] == "text-embedding-ada-002"


class TestGetDocumentWriter:
    def test_creates_store_and_returns_writer(self, ai_service: AIService, mocker: MockerFixture) -> None:
        # given
        mock_store = mocker.MagicMock()
        mocker.patch("knowledge_service.services.ai_service.PgvectorDocumentStore", return_value=mock_store)
        mock_writer = mocker.MagicMock()
        mock_writer_cls = mocker.patch("knowledge_service.services.ai_service.DocumentWriter", return_value=mock_writer)

        # when
        result = ai_service.get_document_writer("my_table", recreate_table=False)

        # then
        assert result is mock_writer
        mock_writer_cls.assert_called_once_with(document_store=mock_store)


class TestGetDocumentRetriever:
    def test_creates_store_if_not_cached(self, ai_service: AIService, mocker: MockerFixture) -> None:
        # given
        mock_store = mocker.MagicMock()
        mocker.patch("knowledge_service.services.ai_service.PgvectorDocumentStore", return_value=mock_store)
        mock_retriever = mocker.MagicMock()
        mocker.patch("knowledge_service.services.ai_service.PgvectorEmbeddingRetriever", return_value=mock_retriever)

        # when
        result = ai_service.get_document_retriever("new_table", top_k=3)

        # then
        assert result is mock_retriever
        assert "new_table" in ai_service._document_stores

    def test_reuses_cached_store(self, ai_service: AIService, mocker: MockerFixture) -> None:
        # given
        mock_store = mocker.MagicMock()
        ai_service._document_stores["existing_table"] = mock_store
        mock_retriever = mocker.MagicMock()
        mock_retriever_cls = mocker.patch(
            "knowledge_service.services.ai_service.PgvectorEmbeddingRetriever", return_value=mock_retriever
        )
        add_store_spy = mocker.spy(ai_service, "add_document_store")

        # when
        ai_service.get_document_retriever("existing_table")

        # then
        add_store_spy.assert_not_called()
        mock_retriever_cls.assert_called_once_with(document_store=mock_store, top_k=5)


class TestProcessDocuments:
    def test_runs_pipeline_and_returns_written_count(self, ai_service: AIService, mocker: MockerFixture) -> None:
        # given
        documents = [Document(content="doc1"), Document(content="doc2")]
        mock_pipeline = mocker.MagicMock()
        mock_pipeline.run.return_value = {"writer": {"documents_written": 2}}
        mocker.patch.object(ai_service, "create_document_pipeline", return_value=mock_pipeline)

        # when
        result = ai_service.process_documents("my_table", documents)

        # then
        assert result == 2
        mock_pipeline.run.assert_called_once_with({"splitter": {"documents": documents}})

    def test_returns_zero_when_pipeline_result_is_empty(self, ai_service: AIService, mocker: MockerFixture) -> None:
        # given
        mock_pipeline = mocker.MagicMock()
        mock_pipeline.run.return_value = {}
        mocker.patch.object(ai_service, "create_document_pipeline", return_value=mock_pipeline)

        # when
        result = ai_service.process_documents("my_table", [])

        # then
        assert result == 0


class TestSearchDocumentsDatabase:
    def test_aggregates_results_from_all_sources(
        self, ai_service: AIService, mock_settings: Settings, mocker: MockerFixture
    ) -> None:
        # given
        source_a = mocker.MagicMock()
        source_a.id = "vault-a"
        source_b = mocker.MagicMock()
        source_b.id = "vault-b"
        mock_settings.obsidian_sources = [source_a, source_b]

        doc_a = Document(content="result from a", score=0.9)
        doc_b = Document(content="result from b", score=0.7)
        mocker.patch.object(
            ai_service,
            "search_documents_table",
            side_effect=[[doc_a], [doc_b]],
        )

        # when
        results = ai_service.search_documents_database("my query", top_k=5)

        # then
        assert len(results) == 2
        assert results[0].score == 0.9  # sorted by score descending
        assert results[1].score == 0.7

    def test_limits_results_to_top_k(
        self, ai_service: AIService, mock_settings: Settings, mocker: MockerFixture
    ) -> None:
        # given
        source = mocker.MagicMock()
        source.id = "vault-1"
        mock_settings.obsidian_sources = [source]

        documents = [Document(content=f"doc{i}", score=float(i)) for i in range(10)]
        mocker.patch.object(ai_service, "search_documents_table", return_value=documents)

        # when
        results = ai_service.search_documents_database("query", top_k=3)

        # then
        assert len(results) == 3

    def test_returns_empty_when_no_sources(self, ai_service: AIService, mock_settings: Settings) -> None:
        # given
        mock_settings.obsidian_sources = []

        # when
        results = ai_service.search_documents_database("query")

        # then
        assert results == []
