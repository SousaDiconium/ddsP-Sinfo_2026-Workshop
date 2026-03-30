from frontend.utils.theme import (
    ACCENT_GREEN,
    ACCENT_ORANGE,
    ACCENT_RED,
    CUSTOM_CSS,
    IST_BLUE,
    apply_theme,
)
from pytest_mock import MockerFixture


class TestColorConstants:
    def test_ist_blue_value(self) -> None:
        assert IST_BLUE == "#009de0"

    def test_accent_green_value(self) -> None:
        assert ACCENT_GREEN == "#00c896"

    def test_accent_orange_value(self) -> None:
        assert ACCENT_ORANGE == "#f59e0b"

    def test_accent_red_value(self) -> None:
        assert ACCENT_RED == "#ef4444"

    def test_all_colors_are_valid_hex(self) -> None:
        # given
        colors = [IST_BLUE, ACCENT_GREEN, ACCENT_ORANGE, ACCENT_RED]

        # then
        for color in colors:
            assert color.startswith("#")
            assert len(color) == 7


class TestCustomCss:
    def test_custom_css_is_non_empty_string(self) -> None:
        assert isinstance(CUSTOM_CSS, str)
        assert len(CUSTOM_CSS) > 0

    def test_custom_css_contains_style_tags(self) -> None:
        assert "<style>" in CUSTOM_CSS
        assert "</style>" in CUSTOM_CSS

    def test_custom_css_references_ist_blue(self) -> None:
        assert IST_BLUE in CUSTOM_CSS


class TestApplyTheme:
    def test_calls_st_markdown_with_custom_css(self, mocker: MockerFixture) -> None:
        # given
        mock_markdown = mocker.patch("streamlit.markdown")

        # when
        apply_theme()

        # then
        mock_markdown.assert_called_once_with(CUSTOM_CSS, unsafe_allow_html=True)

    def test_passes_unsafe_allow_html_true(self, mocker: MockerFixture) -> None:
        # given
        mock_markdown = mocker.patch("streamlit.markdown")

        # when
        apply_theme()

        # then
        _, kwargs = mock_markdown.call_args
        assert kwargs["unsafe_allow_html"] is True
