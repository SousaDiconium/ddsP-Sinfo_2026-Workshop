from pathlib import Path

from streamlit.testing.v1 import AppTest

HELPER_FILE = str(Path(__file__).parent / "_layout_helper.py")


class TestSetupPage:
    def test_renders_without_exception(self) -> None:
        # when
        at = AppTest.from_file(HELPER_FILE)
        at.run()

        # then
        assert not at.exception

    def test_renders_sidebar_branding_and_footer(self) -> None:
        # when
        at = AppTest.from_file(HELPER_FILE)
        at.run()

        # then — two sidebar markdown blocks: branding + footer
        assert len(at.sidebar.markdown) == 2

    def test_sidebar_branding_contains_app_name(self) -> None:
        # when
        at = AppTest.from_file(HELPER_FILE)
        at.run()

        # then
        assert "Trivial Fenix" in at.sidebar.markdown[0].value

    def test_sidebar_footer_contains_diconium(self) -> None:
        # when
        at = AppTest.from_file(HELPER_FILE)
        at.run()

        # then
        assert "diconium" in at.sidebar.markdown[1].value
