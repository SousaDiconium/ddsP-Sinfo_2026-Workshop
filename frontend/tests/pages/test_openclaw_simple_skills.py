from pathlib import Path

from streamlit.testing.v1 import AppTest

PAGE_FILE = str(Path(__file__).parent.parent.parent / "frontend" / "pages" / "openclaw_simple_skills.py")


class TestOpenClawSimpleSkillsPage:
    def test_renders_without_exception(self) -> None:
        at = AppTest.from_file(PAGE_FILE)
        at.run()
        assert not at.exception

    def test_all_four_skills_present(self) -> None:
        at = AppTest.from_file(PAGE_FILE)
        at.run()
        subheaders = [s.value for s in at.subheader]
        assert any("weather" in s.lower() for s in subheaders)
        assert any("knowledge-ingest" in s.lower() or "ingest" in s.lower() for s in subheaders)
        assert any("knowledge-query" in s.lower() or "query" in s.lower() for s in subheaders)
        assert any("vault" in s.lower() for s in subheaders)

    def test_caution_section_present(self) -> None:
        at = AppTest.from_file(PAGE_FILE)
        at.run()
        all_text = " ".join(m.value for m in at.markdown)
        assert "Trust" in all_text or "Caution" in all_text or "caution" in all_text.lower()
