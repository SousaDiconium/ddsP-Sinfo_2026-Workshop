from pathlib import Path

from streamlit.testing.v1 import AppTest

PAGE_FILE = str(Path(__file__).parent.parent.parent / "frontend" / "pages" / "apis_rest.py")


class TestApisRestPage:
    def test_renders_without_exception(self) -> None:
        # when
        at = AppTest.from_file(PAGE_FILE)
        at.run()

        # then
        assert not at.exception

    def test_check_connection_button_exists(self) -> None:
        # when
        at = AppTest.from_file(PAGE_FILE)
        at.run()

        # then
        button_labels = [b.label for b in at.button]
        assert any("Check Connection" in label for label in button_labels)

    def test_api_concepts_content_present(self) -> None:
        # when
        at = AppTest.from_file(PAGE_FILE)
        at.run()

        # then
        rendered = " ".join(m.value for m in at.markdown)
        assert "API" in rendered
