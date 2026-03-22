"""Defines the data models for embedding requests and responses."""

from pydantic import BaseModel


class EmbeddingRequestDTO(BaseModel):
    """
    Represents an embedding request for a single text.

    Attributes:
        text: The text to embed.

    """

    text: str


class EmbeddingResponseDTO(BaseModel):
    """
    Represents the embedding response for a single text.

    Attributes:
        text: The original text.
        embedding: The embedding vector.
        dimensions: The number of dimensions in the embedding.

    """

    text: str
    embedding: list[float]
    dimensions: int


class EmbeddingCompareRequestDTO(BaseModel):
    """
    Represents a request to compare embeddings of multiple texts.

    Attributes:
        texts: A list of texts to embed and compare.

    """

    texts: list[str]


class EmbeddingSimilarityPairDTO(BaseModel):
    """
    Represents the cosine similarity between two texts.

    Attributes:
        text_a: The first text.
        text_b: The second text.
        similarity: The cosine similarity score between the two embeddings.

    """

    text_a: str
    text_b: str
    similarity: float


class EmbeddingCompareResponseDTO(BaseModel):
    """
    Represents the response for an embedding comparison request.

    Attributes:
        embeddings: A list of embedding responses for each input text.
        similarities: A list of pairwise cosine similarity scores.

    """

    embeddings: list[EmbeddingResponseDTO]
    similarities: list[EmbeddingSimilarityPairDTO]
