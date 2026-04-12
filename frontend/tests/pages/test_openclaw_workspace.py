from pathlib import Path

from streamlit.testing.v1 import AppTest

PAGE_FILE = str(Path(__file__).parent.parent.parent / "frontend" / "pages" / "openclaw_workspace.py")


class TestOpenClawWorkspacePage:
    def test_renders_without_exception(self) -> None:
        at = AppTest.from_file(PAGE_FILE)
        at.run()
        assert not at.exception

    def test_workspace_files_section_present(self) -> None:
        at = AppTest.from_file(PAGE_FILE)
        at.run()
        subheaders = [s.value for s in at.subheader]
        assert any("Workspace" in s or "Files" in s for s in subheaders)

    def test_soul_md_mentioned(self) -> None:
        at = AppTest.from_file(PAGE_FILE)
        at.run()
        all_text = " ".join(m.value for m in at.markdown)
        assert "SOUL" in all_text, "Expected SOUL.md to be mentioned on the page"
