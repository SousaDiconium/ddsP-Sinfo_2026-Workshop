from pathlib import Path

from streamlit.testing.v1 import AppTest

APP_FILE = str(Path(__file__).parent.parent / "frontend" / "app.py")


class TestAppNavigation:
    def test_renders_without_exception(self) -> None:
        # when
        at = AppTest.from_file(APP_FILE)
        at.run()

        # then
        assert not at.exception

    def test_welcome_title_is_present(self) -> None:
        # when
        at = AppTest.from_file(APP_FILE)
        at.run()

        # then
        rendered = " ".join(m.value for m in at.markdown)
        assert "Trivial Fenix" in rendered

    def test_sidebar_branding_rendered(self) -> None:
        # when
        at = AppTest.from_file(APP_FILE)
        at.run()

        # then
        assert len(at.sidebar.markdown) >= 1
        assert "Trivial Fenix" in at.sidebar.markdown[0].value
