from pathlib import Path

from streamlit.testing.v1 import AppTest

PAGE_FILE = str(Path(__file__).parent.parent.parent / "frontend" / "pages" / "openclaw_complex_skills.py")


class TestOpenClawComplexSkillsPage:
    def test_renders_without_exception(self) -> None:
        at = AppTest.from_file(PAGE_FILE)
        at.run()
        assert not at.exception

    def test_fenix_login_section_present(self) -> None:
        at = AppTest.from_file(PAGE_FILE)
        at.run()
        subheaders = [s.value for s in at.subheader]
        assert any("fenix-login" in s.lower() or "login" in s.lower() for s in subheaders)

    def test_fenix_browser_section_present(self) -> None:
        at = AppTest.from_file(PAGE_FILE)
        at.run()
        subheaders = [s.value for s in at.subheader]
        assert any("fenix-browser" in s.lower() or "browser" in s.lower() for s in subheaders)

    def test_dependency_chain_or_scripts_mentioned(self) -> None:
        at = AppTest.from_file(PAGE_FILE)
        at.run()
        all_text = " ".join(m.value for m in at.markdown)
        assert "scripts" in all_text.lower() or "dependency" in all_text.lower() or "chain" in all_text.lower()
