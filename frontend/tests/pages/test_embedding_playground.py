from pathlib import Path

from streamlit.testing.v1 import AppTest

PAGE_FILE = str(Path(__file__).parent.parent.parent / "frontend" / "pages" / "3_Embedding_Playground.py")


class TestEmbeddingPlaygroundPage:
    def test_renders_without_exception(self) -> None:
        # when
        at = AppTest.from_file(PAGE_FILE)
        at.run(timeout=30)

        # then
        assert not at.exception

    def test_add_sentence_button_exists(self) -> None:
        # when
        at = AppTest.from_file(PAGE_FILE)
        at.run(timeout=30)

        # then
        button_labels = [b.label for b in at.button]
        assert any("Add sentence" in label for label in button_labels)

    def test_compare_embeddings_button_exists(self) -> None:
        # when
        at = AppTest.from_file(PAGE_FILE)
        at.run(timeout=30)

        # then
        button_labels = [b.label for b in at.button]
        assert any("Compare Embeddings" in label for label in button_labels)

    def test_default_entries_are_pre_populated(self) -> None:
        # when
        at = AppTest.from_file(PAGE_FILE)
        at.run(timeout=30)

        # then — default entries provide text areas
        assert len(at.text_area) >= 1

    def test_renders_sidebar_branding(self) -> None:
        # when
        at = AppTest.from_file(PAGE_FILE)
        at.run(timeout=30)

        # then
        assert "Trivial Fenix" in at.sidebar.markdown[0].value
