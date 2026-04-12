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

    def get_text_embedder(self) -> AzureOpenAITextEmbedder:
        """
        Create and return an AzureOpenAITextEmbedder instance configured with the current settings.

        Returns:
            AzureOpenAITextEmbedder: An instance of the text embedder.

        """
        raise NotImplementedError("Text embedder is not implemented yet.")

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
        raise NotImplementedError("Document splitter is not implemented yet.")

    def get_document_embedder(self) -> AzureOpenAIDocumentEmbedder:
        """
        Create and return an AzureOpenAIDocumentEmbedder instance configured with the current settings.

        Returns:
            AzureOpenAIDocumentEmbedder: An instance of the document embedder.

        """
        raise NotImplementedError("Document embedder is not implemented yet.")

    def get_document_writer(self, table: str, *, recreate_table: bool = True) -> DocumentWriter:
        """
        Create and return a DocumentWriter instance for the specified table.

        Args:
            table (str): The name of the table to be used for the document store.
            recreate_table (bool): Whether to drop and recreate the table. Defaults to True.

        Returns:
            DocumentWriter: An instance of the DocumentWriter component.

        """
        raise NotImplementedError("Document writer is not implemented yet.")

    def get_document_retriever(self, table: str, top_k: int = 5) -> PgvectorEmbeddingRetriever:
        """
        Create and return a PgvectorEmbeddingRetriever instance for the specified table.

        Args:
            table (str): The name of the table to be used for the document store.
            top_k (int, optional): The number of top results to return during retrieval. Defaults to 5.

        Returns:
            PgvectorEmbeddingRetriever: An instance of the PgvectorEmbeddingRetriever component.

        """
        raise NotImplementedError("Document retriever is not implemented yet.")

    def embed_text(self, text: str) -> list[float]:
        """
        Generate an embedding vector for a single text string.

        Args:
            text (str): The text to embed.

        Returns:
            list[float]: The embedding vector for the input text.

        """
        pipeline = Pipeline()

        # Add components to the pipeline in the correct order: text_embedder
        result = {}  # replace with actual pipeline execution under this line once components are implemented
        # result = pipeline.run({"text_embedder": {"text": text}})
        embedding = [0.0, 1.0, 0.5]  # replace with actual embedding result from pipeline execution once implemented
        # embedding: list[float] = result["text_embedder"]["embedding"]

        return embedding

    def process_documents(self, table: str, documents: list[Document], *, recreate_table: bool = True) -> int:
        """
        Process documents through the document processing pipeline for splitting, embedding, and storage.

        Args:
            table (str): The name of the table to be used for the document store.
            documents (list[Document]): A list of Document objects to be processed.
            recreate_table (bool): Whether to drop and recreate the table. Defaults to True.

        Returns:
            int: The number of document chunks written to the store.

        """
        document_pipeline = Pipeline()

        # Add components to the pipeline in the correct order: splitter -> embedder -> writer
        result = {}  # replace with actual pipeline execution under this line once components are implemented
        # result = document_pipeline.run({"splitter": {"documents": documents}})

        return int(result.get("writer", {}).get("documents_written", 0))

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
        query_pipeline = Pipeline()

        # Add components to the pipeline in the correct order: text_embedder -> retriever
        search_results = {}  # replace with actual pipeline execution under this line once components are implemented
        # search_results = query_pipeline.run({"text_embedder": {"text": query}})
        documents = []  # replace with actual documents result from pipeline execution once implemented
        # documents: list[Document] = search_results["retriever"]["documents"]

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
