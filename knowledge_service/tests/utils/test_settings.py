from pathlib import Path

from knowledge_service.utils.settings import Settings, SettingsSource
from pytest_mock import MockerFixture


class TestSettingsSource:
    def test_location_path_with_absolute_path(self, tmp_path: Path) -> None:
        # given
        absolute_path = tmp_path / "absolute_location"
        settings_source = SettingsSource(id="test", location=str(absolute_path), description="Test source")

        # when
        location_path = settings_source.location_path

        # then
        assert location_path == absolute_path

    def test_location_path_with_relative_path(self, tmp_path: Path) -> None:
        # given
        relative_location = "relative_location"
        expected_location = (
            Path(__file__).parent.parent.parent / "knowledge_service" / "resources" / relative_location
        ).resolve()
        settings_source = SettingsSource(id="test", location=relative_location, description="Test source")

        # when
        location_path = settings_source.location_path

        # then
        assert location_path == expected_location


class TestSettings:
    def test_settings_customise_sources_prioritizes_env_and_yaml(self, mocker: MockerFixture) -> None:
        # given
        mock_settings_cls = mocker.Mock()
        mock_init_settings = mocker.Mock()
        mock_env_settings = mocker.Mock()
        mock_dotenv_settings = mocker.Mock()
        mock_file_secret_settings = mocker.Mock()

        mock_yaml_settings = mocker.patch("knowledge_service.utils.settings.YamlConfigSettingsSource")

        # when
        sources = Settings.settings_customise_sources(
            mock_settings_cls,
            mock_init_settings,
            mock_env_settings,
            mock_dotenv_settings,
            mock_file_secret_settings,
        )

        # then
        mock_yaml_settings.assert_called_once()
        mock_yaml_settings.assert_called_with(mock_settings_cls)

        assert sources[0] == mock_env_settings
        assert sources[1] == mock_dotenv_settings
        assert sources[2] == mock_init_settings
        assert sources[3] == mock_yaml_settings.return_value
