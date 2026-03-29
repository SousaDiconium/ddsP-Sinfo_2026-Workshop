import pytest
from knowledge_service.models.answer import KnowledgeAnswerDTO, SourceDTO
from pydantic import ValidationError


class TestSourceDTO:
    def test_instantiation(self) -> None:
        # given / when
        source = SourceDTO(type="document", title="My Doc", link="https://example.com")

        # then
        assert source.type == "document"
        assert source.title == "My Doc"
        assert source.link == "https://example.com"

    def test_missing_required_field_raises(self) -> None:
        # when / then
        with pytest.raises(ValidationError):
            SourceDTO(type="document", title="My Doc")  # type: ignore[call-arg]  # missing link


class TestKnowledgeAnswerDTO:
    def test_instantiation(self) -> None:
        # given
        source = SourceDTO(type="document", title="Doc", link="http://link")

        # when
        answer = KnowledgeAnswerDTO(content="The answer.", source=source)

        # then
        assert answer.content == "The answer."
        assert answer.source.type == "document"

    def test_missing_content_raises(self) -> None:
        # given
        source = SourceDTO(type="document", title="Doc", link="http://link")

        # when / then
        with pytest.raises(ValidationError):
            KnowledgeAnswerDTO(source=source)  # type: ignore[call-arg]  # missing content
