import pytest
from knowledge_service.models.document_table import (
    CreateTableRequestDTO,
    DocumentTableDTO,
    FileUploadResponseDTO,
)
from pydantic import ValidationError


class TestDocumentTableDTO:
    def test_instantiation(self) -> None:
        # given / when
        dto = DocumentTableDTO(source="my_table", document_count=100)

        # then
        assert dto.source == "my_table"
        assert dto.document_count == 100

    def test_missing_field_raises(self) -> None:
        # when / then
        with pytest.raises(ValidationError):
            DocumentTableDTO(source="my_table")  # type: ignore[call-arg]  # missing document_count


class TestCreateTableRequestDTO:
    def test_instantiation(self) -> None:
        # given / when
        dto = CreateTableRequestDTO(table_name="new_table")

        # then
        assert dto.table_name == "new_table"

    def test_missing_field_raises(self) -> None:
        # when / then
        with pytest.raises(ValidationError):
            CreateTableRequestDTO()  # type: ignore[call-arg]  # missing table_name


class TestFileUploadResponseDTO:
    def test_instantiation(self) -> None:
        # given / when
        dto = FileUploadResponseDTO(
            table_name="my_table",
            file_name="doc.md",
            chunks_created=5,
            message="Successfully ingested.",
        )

        # then
        assert dto.table_name == "my_table"
        assert dto.file_name == "doc.md"
        assert dto.chunks_created == 5
        assert dto.message == "Successfully ingested."

    def test_missing_field_raises(self) -> None:
        # when / then
        with pytest.raises(ValidationError):
            FileUploadResponseDTO(table_name="t", file_name="f.md", chunks_created=1)  # type: ignore[call-arg]  # missing message
