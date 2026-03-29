import pytest
from knowledge_service.models.message import MessageDTO
from pydantic import ValidationError


class TestMessageDTO:
    def test_instantiation(self) -> None:
        # given / when
        msg = MessageDTO(content="Hello everyone!", timestamp="2024-01-01T00:00:00")

        # then
        assert msg.content == "Hello everyone!"
        assert msg.timestamp == "2024-01-01T00:00:00"

    def test_missing_timestamp_raises(self) -> None:
        # when / then
        with pytest.raises(ValidationError):
            MessageDTO(content="Only content")  # type: ignore[call-arg]  # missing timestamp

    def test_missing_content_raises(self) -> None:
        # when / then
        with pytest.raises(ValidationError):
            MessageDTO(timestamp="2024-01-01T00:00:00")  # type: ignore[call-arg]  # missing content
