from knowledge_service.models.document import DocumentDTO, DocumentMetaDTO, PaginatedDocumentDTO


class TestDocumentMetaDTO:
    def test_all_fields_are_optional(self) -> None:
        # when
        meta = DocumentMetaDTO()

        # then
        assert meta.when is None
        assert meta.title is None
        assert meta.source is None
        assert meta.split_id is None

    def test_instantiation_with_all_fields(self) -> None:
        # given / when
        meta = DocumentMetaDTO(
            when="2024-01-01",
            title="My Doc",
            source="/path/to/doc.md",
            split_id=2,
            source_id="src-1",
            page_number=3,
            split_idx_start=0,
        )

        # then
        assert meta.when == "2024-01-01"
        assert meta.title == "My Doc"
        assert meta.source == "/path/to/doc.md"
        assert meta.split_id == 2


class TestDocumentDTO:
    def test_from_orm_maps_all_fields(self) -> None:
        # given
        class FakeOrm:
            id = "doc-1"
            content = "Some content"
            blob_mime_type = "text/plain"
            meta = {"source": "/path/doc.md", "title": "My Doc"}

        # when
        dto = DocumentDTO.from_orm(FakeOrm())

        # then
        assert dto.id == "doc-1"
        assert dto.content == "Some content"
        assert dto.blob_mime_type == "text/plain"
        assert dto.meta.source == "/path/doc.md"
        assert dto.meta.title == "My Doc"

    def test_from_orm_handles_empty_meta(self) -> None:
        # given
        class FakeOrm:
            id = "doc-2"
            content = "Content"
            blob_mime_type = None
            meta: dict[str, object] = {}

        # when
        dto = DocumentDTO.from_orm(FakeOrm())

        # then
        assert dto.id == "doc-2"
        assert dto.meta.source is None
        assert dto.meta.title is None

    def test_from_orm_handles_none_meta(self) -> None:
        # given
        class FakeOrm:
            id = "doc-3"
            content = "Content"
            blob_mime_type = None
            meta = None

        # when
        dto = DocumentDTO.from_orm(FakeOrm())

        # then
        assert dto.meta.source is None

    def test_from_orm_ignores_unknown_meta_keys(self) -> None:
        # given
        class FakeOrm:
            id = "doc-4"
            content = "Content"
            blob_mime_type = None
            meta = {"source": "/doc.md", "unknown_key": "should_be_ignored"}

        # when
        dto = DocumentDTO.from_orm(FakeOrm())

        # then
        assert dto.meta.source == "/doc.md"


class TestPaginatedDocumentDTO:
    def test_instantiation(self) -> None:
        # given
        meta = DocumentMetaDTO(source="/doc.md")
        doc = DocumentDTO(id="1", content="text", blob_mime_type=None, meta=meta)

        # when
        paginated = PaginatedDocumentDTO(page=1, page_size=10, total=1, items=[doc])

        # then
        assert paginated.page == 1
        assert paginated.page_size == 10
        assert paginated.total == 1
        assert len(paginated.items) == 1

    def test_empty_items(self) -> None:
        # when
        paginated = PaginatedDocumentDTO(page=1, page_size=10, total=0, items=[])

        # then
        assert paginated.items == []
        assert paginated.total == 0
