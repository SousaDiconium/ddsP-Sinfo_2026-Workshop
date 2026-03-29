import pytest
from knowledge_service.models.embedding import (
    EmbeddingCompareRequestDTO,
    EmbeddingCompareResponseDTO,
    EmbeddingRequestDTO,
    EmbeddingResponseDTO,
    EmbeddingSimilarityPairDTO,
)
from pydantic import ValidationError


class TestEmbeddingRequestDTO:
    def test_instantiation(self) -> None:
        # given / when
        dto = EmbeddingRequestDTO(text="hello world")

        # then
        assert dto.text == "hello world"

    def test_missing_field_raises(self) -> None:
        # when / then
        with pytest.raises(ValidationError):
            EmbeddingRequestDTO()  # type: ignore[call-arg]  # missing text


class TestEmbeddingResponseDTO:
    def test_instantiation(self) -> None:
        # given / when
        dto = EmbeddingResponseDTO(text="hello", embedding=[0.1, 0.2, 0.3], dimensions=3)

        # then
        assert dto.text == "hello"
        assert dto.embedding == [0.1, 0.2, 0.3]
        assert dto.dimensions == 3


class TestEmbeddingCompareRequestDTO:
    def test_instantiation(self) -> None:
        # given / when
        dto = EmbeddingCompareRequestDTO(texts=["text a", "text b", "text c"])

        # then
        assert len(dto.texts) == 3
        assert dto.texts[0] == "text a"

    def test_empty_list(self) -> None:
        # given / when
        dto = EmbeddingCompareRequestDTO(texts=[])

        # then
        assert dto.texts == []


class TestEmbeddingSimilarityPairDTO:
    def test_instantiation(self) -> None:
        # given / when
        dto = EmbeddingSimilarityPairDTO(text_a="hello", text_b="world", similarity=0.95)

        # then
        assert dto.text_a == "hello"
        assert dto.text_b == "world"
        assert dto.similarity == 0.95


class TestEmbeddingCompareResponseDTO:
    def test_instantiation(self) -> None:
        # given
        emb_a = EmbeddingResponseDTO(text="a", embedding=[0.1], dimensions=1)
        emb_b = EmbeddingResponseDTO(text="b", embedding=[0.2], dimensions=1)
        pair = EmbeddingSimilarityPairDTO(text_a="a", text_b="b", similarity=0.8)

        # when
        dto = EmbeddingCompareResponseDTO(embeddings=[emb_a, emb_b], similarities=[pair])

        # then
        assert len(dto.embeddings) == 2
        assert len(dto.similarities) == 1
        assert dto.similarities[0].similarity == 0.8

    def test_empty_embeddings_and_similarities(self) -> None:
        # when
        dto = EmbeddingCompareResponseDTO(embeddings=[], similarities=[])

        # then
        assert dto.embeddings == []
        assert dto.similarities == []
