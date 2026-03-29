from knowledge_service.entities.document_embedding import document_model_factory


class TestDocumentModelFactory:
    def test_returns_class_with_correct_tablename(self) -> None:
        # when
        model = document_model_factory("entity_test_table")

        # then
        assert model.__tablename__ == "entity_test_table"

    def test_class_name_includes_table_name(self) -> None:
        # when
        model = document_model_factory("entity_named_table")

        # then
        assert "entity_named_table" in model.__name__

    def test_caches_class_for_same_table_name(self) -> None:
        # when
        model_a = document_model_factory("entity_cached_table")
        model_b = document_model_factory("entity_cached_table")

        # then
        assert model_a is model_b

    def test_returns_different_classes_for_different_table_names(self) -> None:
        # when
        model_a = document_model_factory("entity_table_alpha")
        model_b = document_model_factory("entity_table_beta")

        # then
        assert model_a is not model_b
        assert model_a.__tablename__ == "entity_table_alpha"
        assert model_b.__tablename__ == "entity_table_beta"
