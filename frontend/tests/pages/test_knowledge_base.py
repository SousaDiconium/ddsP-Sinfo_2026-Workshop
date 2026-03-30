from pathlib import Path

from pytest_mock import MockerFixture
from streamlit.testing.v1 import AppTest

PAGE_FILE = str(Path(__file__).parent.parent.parent / "frontend" / "pages" / "1_Knowledge_Base.py")


class TestKnowledgeBasePage:
    def test_renders_without_exception_when_no_data(self, mocker: MockerFixture) -> None:
        # given
        mocker.patch("frontend.utils.api.list_document_tables", return_value=[])
        mocker.patch("frontend.utils.api.list_vaults", return_value=[])

        # when
        at = AppTest.from_file(PAGE_FILE)
        at.run()

        # then
        assert not at.exception

    def test_shows_info_when_no_tables(self, mocker: MockerFixture) -> None:
        # given
        mocker.patch("frontend.utils.api.list_document_tables", return_value=[])
        mocker.patch("frontend.utils.api.list_vaults", return_value=[])

        # when
        at = AppTest.from_file(PAGE_FILE)
        at.run()

        # then
        info_text = " ".join(i.value for i in at.info)
        assert "No document tables" in info_text

    def test_shows_warning_when_no_vaults(self, mocker: MockerFixture) -> None:
        # given
        mocker.patch("frontend.utils.api.list_document_tables", return_value=[])
        mocker.patch("frontend.utils.api.list_vaults", return_value=[])

        # when
        at = AppTest.from_file(PAGE_FILE)
        at.run()

        # then
        warning_text = " ".join(w.value for w in at.warning)
        assert "No vaults" in warning_text

    def test_renders_without_exception_with_tables_and_vaults(self, mocker: MockerFixture) -> None:
        # given
        mocker.patch(
            "frontend.utils.api.list_document_tables",
            return_value=[{"source": "my_vault", "document_count": 10}],
        )
        mocker.patch(
            "frontend.utils.api.list_vaults",
            return_value=[{"id": "my_vault", "location": "/path", "description": "Test vault"}],
        )

        # when
        at = AppTest.from_file(PAGE_FILE)
        at.run()

        # then
        assert not at.exception

    def test_renders_sidebar_branding(self, mocker: MockerFixture) -> None:
        # given
        mocker.patch("frontend.utils.api.list_document_tables", return_value=[])
        mocker.patch("frontend.utils.api.list_vaults", return_value=[])

        # when
        at = AppTest.from_file(PAGE_FILE)
        at.run()

        # then
        assert "Trivial Fenix" in at.sidebar.markdown[0].value
