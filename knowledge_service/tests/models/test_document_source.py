import pytest
from knowledge_service.models.document_source import DocumentSourceDTO, PaginatedDocumentSourceDTO
from pydantic import ValidationError


class TestDocumentSourceDTO:
    def test_instantiation(self) -> None:
        # given / when
        source = DocumentSourceDTO(id="src-1", title="Source One", number_documents=42)

        # then
        assert source.id == "src-1"
        assert source.title == "Source One"
        assert source.number_documents == 42

    def test_missing_field_raises(self) -> None:
        # when / then
        with pytest.raises(ValidationError):
            DocumentSourceDTO(id="src-1", title="Source One")  # type: ignore[call-arg]  # missing number_documents


class TestPaginatedDocumentSourceDTO:
    def test_instantiation(self) -> None:
        # given
        item = DocumentSourceDTO(id="s1", title="T", number_documents=5)

        # when
        paginated = PaginatedDocumentSourceDTO(page=2, page_size=10, total=50, items=[item])

        # then
        assert paginated.page == 2
        assert paginated.page_size == 10
        assert paginated.total == 50
        assert len(paginated.items) == 1

    def test_empty_items(self) -> None:
        # when
        paginated = PaginatedDocumentSourceDTO(page=1, page_size=10, total=0, items=[])

        # then
        assert paginated.items == []
