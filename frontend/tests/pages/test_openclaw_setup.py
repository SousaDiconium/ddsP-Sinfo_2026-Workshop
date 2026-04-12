from pathlib import Path

from streamlit.testing.v1 import AppTest

PAGE_FILE = str(Path(__file__).parent.parent.parent / "frontend" / "pages" / "openclaw_setup.py")


class TestOpenClawSetupPage:
    def test_renders_without_exception(self) -> None:
        at = AppTest.from_file(PAGE_FILE)
        at.run()
        assert not at.exception

    def test_models_json_present(self) -> None:
        at = AppTest.from_file(PAGE_FILE)
        at.run()
        code_blocks = [c.value for c in at.code if "gpt-5.3-codex" in c.value]
        assert code_blocks, "Expected gpt-5.3-codex to appear in a code block"

    def test_step_headings_present(self) -> None:
        at = AppTest.from_file(PAGE_FILE)
        at.run()
        subheaders = [s.value for s in at.subheader]
        assert any("Step 1" in s for s in subheaders)
        assert any("Step 2" in s for s in subheaders)
