from typing import cast
from unittest.mock import MagicMock as MagicMockType

import pytest
from knowledge_service.services.db_service import DatabaseService
from knowledge_service.utils.settings import Settings
from pytest_mock import MockerFixture
from sqlalchemy import Engine


@pytest.fixture
def mock_engine(mocker: MockerFixture) -> MagicMockType:
    return cast(MagicMockType, mocker.MagicMock())


@pytest.fixture
def db_service(mocker: MockerFixture, mock_engine: MagicMockType) -> DatabaseService:
    mocker.patch("knowledge_service.services.db_service.create_engine", return_value=mock_engine)
    mock_settings = mocker.MagicMock(spec=Settings)
    mock_settings.postgres_connection_string = "postgresql://test:test@localhost/test"
    service = DatabaseService(mock_settings)
    service._engine = cast(Engine, mock_engine)
    return service


class TestValidateTableName:
    def test_valid_name_passes(self, db_service: DatabaseService) -> None:
        # when / then (no exception raised)
        db_service._validate_table_name("valid_table_name")
        db_service._validate_table_name("table-with-dashes")
        db_service._validate_table_name("Table123")

    def test_name_with_spaces_raises(self, db_service: DatabaseService) -> None:
        # when / then
        with pytest.raises(ValueError, match="Invalid table name"):
            db_service._validate_table_name("invalid table")

    def test_name_with_semicolon_raises(self, db_service: DatabaseService) -> None:
        # when / then
        with pytest.raises(ValueError, match="Invalid table name"):
            db_service._validate_table_name("table; DROP TABLE users")

    def test_name_with_dot_raises(self, db_service: DatabaseService) -> None:
        # when / then
        with pytest.raises(ValueError, match="Invalid table name"):
            db_service._validate_table_name("schema.table")

    def test_empty_string_raises(self, db_service: DatabaseService) -> None:
        # when / then
        with pytest.raises(ValueError, match="Invalid table name"):
            db_service._validate_table_name("")


class TestCheckTableExists:
    def test_returns_true_when_table_exists(self, db_service: DatabaseService, mock_engine: object) -> None:
        # given
        mock_connection = mock_engine.connect.return_value.__enter__.return_value  # type: ignore[attr-defined]
        mock_result = mock_connection.execute.return_value
        mock_result.scalar.return_value = True

        # when
        result = db_service.check_table_exists("my_table")

        # then
        assert result is True

    def test_returns_false_when_table_does_not_exist(self, db_service: DatabaseService, mock_engine: object) -> None:
        # given
        mock_connection = mock_engine.connect.return_value.__enter__.return_value  # type: ignore[attr-defined]
        mock_result = mock_connection.execute.return_value
        mock_result.scalar.return_value = False

        # when
        result = db_service.check_table_exists("missing_table")

        # then
        assert result is False

    def test_validates_table_name(self, db_service: DatabaseService) -> None:
        # when / then
        with pytest.raises(ValueError, match="Invalid table name"):
            db_service.check_table_exists("bad name!")


class TestCreateTable:
    def test_raises_if_table_already_exists(self, db_service: DatabaseService, mocker: MockerFixture) -> None:
        # given
        mocker.patch.object(db_service, "check_table_exists", return_value=True)

        # when / then
        with pytest.raises(ValueError, match="already exists"):
            db_service.create_table("existing_table")

    def test_executes_create_statement_when_table_does_not_exist(
        self, db_service: DatabaseService, mock_engine: object, mocker: MockerFixture
    ) -> None:
        # given
        mocker.patch.object(db_service, "check_table_exists", return_value=False)
        mock_connection = mock_engine.connect.return_value.__enter__.return_value  # type: ignore[attr-defined]

        # when
        db_service.create_table("new_table")

        # then
        mock_connection.execute.assert_called_once()
        mock_connection.commit.assert_called_once()

    def test_validates_table_name(self, db_service: DatabaseService) -> None:
        # when / then
        with pytest.raises(ValueError, match="Invalid table name"):
            db_service.create_table("bad name!")


class TestDropTable:
    def test_raises_if_table_does_not_exist(self, db_service: DatabaseService, mocker: MockerFixture) -> None:
        # given
        mocker.patch.object(db_service, "check_table_exists", return_value=False)

        # when / then
        with pytest.raises(ValueError, match="does not exist"):
            db_service.drop_table("nonexistent_table")

    def test_executes_drop_statement_when_table_exists(
        self, db_service: DatabaseService, mock_engine: object, mocker: MockerFixture
    ) -> None:
        # given
        mocker.patch.object(db_service, "check_table_exists", return_value=True)
        mock_connection = mock_engine.connect.return_value.__enter__.return_value  # type: ignore[attr-defined]

        # when
        db_service.drop_table("existing_table")

        # then
        mock_connection.execute.assert_called_once()
        mock_connection.commit.assert_called_once()

    def test_validates_table_name(self, db_service: DatabaseService) -> None:
        # when / then
        with pytest.raises(ValueError, match="Invalid table name"):
            db_service.drop_table("bad name!")
