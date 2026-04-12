from pathlib import Path

from pytest_mock import MockerFixture
from streamlit.testing.v1 import AppTest

PAGE_FILE = str(Path(__file__).parent.parent.parent / "frontend" / "pages" / "rag_in_action.py")


class TestRagInActionPage:
    def test_renders_without_exception_when_no_data(self, mocker: MockerFixture) -> None:
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
            return_value=[{"source": "my_vault", "document_count": 10}],
        )

        # when
        at = AppTest.from_file(PAGE_FILE)
        at.run()

        # then
        assert not at.exception
