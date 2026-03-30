from pathlib import Path

from pytest_mock import MockerFixture
from streamlit.testing.v1 import AppTest

PAGE_FILE = str(Path(__file__).parent.parent.parent / "frontend" / "pages" / "4_Table_Management.py")


class TestTableManagementPage:
    def test_renders_without_exception_when_no_tables(self, mocker: MockerFixture) -> None:
        # given
        mocker.patch("frontend.utils.api.list_document_tables", return_value=[])

        # when
        at = AppTest.from_file(PAGE_FILE)
        at.run()

        # then
        assert not at.exception

    def test_create_button_exists(self, mocker: MockerFixture) -> None:
        # given
        mocker.patch("frontend.utils.api.list_document_tables", return_value=[])

        # when
        at = AppTest.from_file(PAGE_FILE)
        at.run()

        # then
        button_labels = [b.label for b in at.button]
        assert "Create" in button_labels

    def test_shows_info_when_no_tables_for_delete(self, mocker: MockerFixture) -> None:
        # given
        mocker.patch("frontend.utils.api.list_document_tables", return_value=[])

        # when
        at = AppTest.from_file(PAGE_FILE)
        at.run()

        # then
        info_text = " ".join(i.value for i in at.info)
        assert "No tables" in info_text

    def test_renders_without_exception_with_tables(self, mocker: MockerFixture) -> None:
        # given
        mocker.patch(
            "frontend.utils.api.list_document_tables",
            return_value=[{"source": "my_table", "document_count": 3}],
        )

        # when
        at = AppTest.from_file(PAGE_FILE)
        at.run()

        # then
        assert not at.exception

    def test_renders_sidebar_branding(self, mocker: MockerFixture) -> None:
        # given
        mocker.patch("frontend.utils.api.list_document_tables", return_value=[])

        # when
        at = AppTest.from_file(PAGE_FILE)
        at.run()

        # then
        assert "Trivial Fenix" in at.sidebar.markdown[0].value
