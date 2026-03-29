import pytest
from knowledge_service.models.query import KnowledgeQueryDTO
from pydantic import ValidationError


class TestKnowledgeQueryDTO:
    def test_default_top_k(self) -> None:
        # given / when
        dto = KnowledgeQueryDTO(query="What is AI?")

        # then
        assert dto.top_k == 5

    def test_custom_top_k(self) -> None:
        # given / when
        dto = KnowledgeQueryDTO(query="What is AI?", top_k=10)

        # then
        assert dto.top_k == 10

    def test_top_k_minimum_boundary(self) -> None:
        # given / when
        dto = KnowledgeQueryDTO(query="test", top_k=1)

        # then
        assert dto.top_k == 1

    def test_top_k_maximum_boundary(self) -> None:
        # given / when
        dto = KnowledgeQueryDTO(query="test", top_k=50)

        # then
        assert dto.top_k == 50

    def test_top_k_below_minimum_raises(self) -> None:
        # when / then
        with pytest.raises(ValidationError):
            KnowledgeQueryDTO(query="test", top_k=0)

    def test_top_k_above_maximum_raises(self) -> None:
        # when / then
        with pytest.raises(ValidationError):
            KnowledgeQueryDTO(query="test", top_k=51)

    def test_missing_query_raises(self) -> None:
        # when / then
        with pytest.raises(ValidationError):
            KnowledgeQueryDTO()  # type: ignore[call-arg]  # missing query
