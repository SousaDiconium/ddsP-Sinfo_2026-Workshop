from pathlib import Path

from streamlit.testing.v1 import AppTest

PAGE_FILE = str(Path(__file__).parent.parent.parent / "frontend" / "pages" / "openclaw_intro.py")


class TestOpenClawIntroPage:
    def test_renders_without_exception(self) -> None:
        at = AppTest.from_file(PAGE_FILE)
        at.run()
        assert not at.exception

    def test_dashboard_link_present(self) -> None:
        at = AppTest.from_file(PAGE_FILE)
        at.run()
        html_blocks = [m.value for m in at.markdown if "18789" in m.value]
        assert html_blocks, "Expected dashboard URL to appear on the page"

    def test_key_concepts_section_present(self) -> None:
        at = AppTest.from_file(PAGE_FILE)
        at.run()
        headings = [m.value for m in at.markdown if "Key Concepts" in m.value or "Concepts" in m.value]
        subheaders = [s.value for s in at.subheader if "Concept" in s.value]
        assert headings or subheaders, "Expected Key Concepts section"
