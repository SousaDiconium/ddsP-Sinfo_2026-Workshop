from pathlib import Path

from pytest_mock import MockerFixture
from streamlit.testing.v1 import AppTest

PAGE_FILE = str(Path(__file__).parent.parent.parent / "frontend" / "pages" / "explore_data.py")


class TestDocumentExplorerPage:
    def test_renders_without_exception_when_no_tables(self, mocker: MockerFixture) -> None:
        # given
        mocker.patch("frontend.utils.api.list_document_tables", return_value=[])

        # when
        at = AppTest.from_file(PAGE_FILE)
        at.run()

        # then
        assert not at.exception

    def test_shows_info_when_no_tables(self, mocker: MockerFixture) -> None:
        # given
        mocker.patch("frontend.utils.api.list_document_tables", return_value=[])

        # when
        at = AppTest.from_file(PAGE_FILE)
        at.run()

        # then
        info_text = " ".join(i.value for i in at.info)
        assert "No document tables" in info_text

    def test_renders_without_exception_with_tables(self, mocker: MockerFixture) -> None:
        # given
        mocker.patch(
            "frontend.utils.api.list_document_tables",
            return_value=[{"source": "my_table", "document_count": 5}],
        )
        mocker.patch(
            "frontend.utils.api.list_document_sources",
            return_value={"items": [], "total": 0},
        )

        # when
        at = AppTest.from_file(PAGE_FILE)
        at.run()

        # then
        assert not at.exception
