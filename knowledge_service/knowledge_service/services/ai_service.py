"""
AI service module.

This module provides the AIService class for managing AI-related operations,
including document embedding, splitting, and storage using PgvectorDocumentStore.
"""

from haystack import Document, Pipeline
from haystack.components.embedders import (
    AzureOpenAIDocumentEmbedder,
    AzureOpenAITextEmbedder,
)
from haystack.components.preprocessors import DocumentSplitter
from haystack.components.writers import DocumentWriter
from haystack.utils import Secret
from haystack_integrations.components.retrievers.pgvector import PgvectorEmbeddingRetriever
from haystack_integrations.document_stores.pgvector import PgvectorDocumentStore
from knowledge_service.utils.settings import Settings


class AIService:
    """
    Service class for managing AI-related operations.

    This class provides methods to create document embedders, text embedders,
    document splitters, and manage PgvectorDocumentStore instances for storing
    and retrieving documents.
    """

    _settings: Settings
    _document_stores: dict[str, PgvectorDocumentStore]

    def __init__(self, settings: Settings) -> None:
        """
        Initialize the AIService with the provided settings and set up internal data structures.

        Args:
            settings (dicopilot.settings.Settings): The settings object containing configuration values.
            document_stores (dict[str, PgvectorDocumentStore]): A dictionary to hold PgvectorDocumentStore instances.

        """
        self._settings = settings
        self._document_stores = {}

    def add_document_store(self, table_name: str, *, recreate_table: bool = False) -> PgvectorDocumentStore:
        """
        Create and add a PgvectorDocumentStore for the specified table name.

        Args:
            table_name (str): The name of the table for which to create the document store.
            recreate_table (bool, optional): Whether to recreate the table if it exists. Defaults to False.

        Returns:
            PgvectorDocumentStore: The created document store instance.

        """
        document_store = PgvectorDocumentStore(
            connection_string=Secret.from_token(self._settings.postgres_connection_string),
            table_name=table_name,
            hnsw_index_name=f"{table_name}_hnsw_index",
            keyword_index_name=f"{table_name}_keyword_index",
            embedding_dimension=self._settings.azure_openai_embeddings_embedding_dimension,
            recreate_table=recreate_table,
        )
        self._document_stores[table_name] = document_store

        return document_store

    def get_document_splitter(self) -> DocumentSplitter:
        """
        Create and return a DocumentSplitter configured to split documents by words.

        Returns:
            DocumentSplitter: An instance configured with split_by="word", split_length=100, and split_overlap=30.

        """
        return DocumentSplitter(split_by="word", split_length=100, split_overlap=30)

    def get_document_embedder(self) -> AzureOpenAIDocumentEmbedder:
        """
        Create and return an AzureOpenAIDocumentEmbedder instance configured with the current settings.

        Returns:
            AzureOpenAIDocumentEmbedder: An instance of the document embedder.

        """
        return AzureOpenAIDocumentEmbedder(
            api_key=Secret.from_token(self._settings.azure_openai_embeddings_api_key),
            api_version=self._settings.azure_openai_embeddings_api_version,
            azure_endpoint=self._settings.azure_openai_embeddings_endpoint,
            azure_deployment=self._settings.azure_openai_embeddings_deployment_name,
        )

    def get_document_writer(self, table: str) -> DocumentWriter:
        """
        Create and return a DocumentWriter instance for the specified table.

        Args:
            table (str): The name of the table to be used for the document store.

        Returns:
            DocumentWriter: An instance of the DocumentWriter component.

        """
        self.add_document_store(table, recreate_table=True)
        document_store = self._document_stores[table]

        return DocumentWriter(document_store=document_store)

    def get_text_embedder(self) -> AzureOpenAITextEmbedder:
        """
        Create and return an AzureOpenAITextEmbedder instance configured with the current settings.

        Returns:
            AzureOpenAITextEmbedder: An instance of the text embedder.

        """
        return AzureOpenAITextEmbedder(
            api_key=Secret.from_token(self._settings.azure_openai_embeddings_api_key),
            api_version=self._settings.azure_openai_embeddings_api_version,
            azure_endpoint=self._settings.azure_openai_embeddings_endpoint,
            azure_deployment=self._settings.azure_openai_embeddings_deployment_name,
        )

    def get_document_retriever(self, table: str, top_k: int = 5) -> PgvectorEmbeddingRetriever:
        """
        Create and return a PgvectorEmbeddingRetriever instance for the specified table.

        Args:
            table (str): The name of the table to be used for the document store.
            top_k (int, optional): The number of top results to return during retrieval. Defaults to 5.

        Returns:
            PgvectorEmbeddingRetriever: An instance of the PgvectorEmbeddingRetriever component.

        """
        if table not in self._document_stores:
            self.add_document_store(table)

        document_store = self._document_stores[table]

        return PgvectorEmbeddingRetriever(document_store=document_store, top_k=top_k)

    def create_document_pipeline(self, table: str) -> Pipeline:
        """
        Create and return a document processing pipeline for the specified table.

        Args:
            table (str): The name of the table to be used for the document store.

        Returns:
            Pipeline: The created document processing pipeline.

        """
        document_splitter = self.get_document_splitter()
        document_embedder = self.get_document_embedder()
        document_writer = self.get_document_writer(table)

        document_pipeline = Pipeline()
        document_pipeline.add_component("splitter", document_splitter)
        document_pipeline.add_component("embedder", document_embedder)
        document_pipeline.add_component("writer", document_writer)

        document_pipeline.connect("splitter", "embedder")
        document_pipeline.connect("embedder", "writer")

        return document_pipeline

    def process_documents(self, table: str, documents: list[Document]) -> None:
        """
        Process documents through the document processing pipeline for splitting, embedding, and storage.

        Args:
            table (str): The name of the table to be used for the document store.
            documents (list[Document]): A list of Document objects to be processed.

        """
        pipeline = self.create_document_pipeline(table)
        pipeline.run({"splitter": {"documents": documents}})

    def embed_text(self, text: str) -> list[float]:
        """
        Generate an embedding vector for a single text string.

        Args:
            text (str): The text to embed.

        Returns:
            list[float]: The embedding vector for the input text.

        """
        text_embedder = self.get_text_embedder()

        pipeline = Pipeline()
        pipeline.add_component("text_embedder", text_embedder)

        result = pipeline.run({"text_embedder": {"text": text}})
        embedding: list[float] = result["text_embedder"]["embedding"]

        return embedding

    def search_documents_table(self, table: str, query: str, top_k: int = 5) -> list[Document]:
        """
        Search for documents in the specified table using a query string.

        Args:
            table (str): The name of the table to search in.
            query (str): The query string to search for.
            top_k (int, optional): The number of top results to return. Defaults to 5.

        Returns:
            list[Document]: A list of Document objects matching the search query.

        """
        text_embedder = self.get_text_embedder()
        retriever = self.get_document_retriever(table, top_k=top_k)

        query_pipeline = Pipeline()
        query_pipeline.add_component("text_embedder", text_embedder)
        query_pipeline.add_component("retriever", retriever)

        query_pipeline.connect("text_embedder.embedding", "retriever.query_embedding")

        search_results = query_pipeline.run({"text_embedder": {"text": query}})

        documents: list[Document] = search_results["retriever"]["documents"]

        return documents

    def search_documents_database(self, query: str, top_k: int = 5) -> list[Document]:
        """
        Search for documents across all tables in the document store using a query string.

        Args:
            query (str): The query string to search for.
            top_k (int, optional): The number of top results to return from each table. Defaults to 5.

        Returns:
            list[Document]: A list of Document objects matching the search query across all tables.

        """
        all_documents = []
        for source in self._settings.obsidian_sources:
            source_table_name = source.id
            documents = self.search_documents_table(source_table_name, query, top_k=top_k)
            all_documents.extend(documents)

        all_documents.sort(key=lambda doc: doc.score if doc.score is not None else float("-inf"), reverse=True)
        all_documents = all_documents[:top_k]

        return all_documents
