"""Defines the settings for the knowledge service application."""

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource, SettingsConfigDict, YamlConfigSettingsSource

current_path = Path(__file__)
resources_path = current_path.parent.parent / "resources"


class Settings(BaseSettings):
    """
    Settings for the application.

    This class defines the configuration settings for the knowledge service application, including log level,
    Additionally it includes settings for Azure OpenAI embeddings, database connection.
    """

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """Customize the order of settings sources to prioritize environment variables and YAML configuration files."""
        return (
            env_settings,
            dotenv_settings,
            init_settings,
            YamlConfigSettingsSource(settings_cls),
        )

    model_config = SettingsConfigDict(
        env_file=resources_path / ".env",
        env_file_encoding="utf-8",
        yaml_file=resources_path / "config.yaml",
        yaml_file_encoding="utf-8",
    )

    # General settings
    log_level: str = Field("INFO", description="The logging level for the application.")

    # Fenix scraper settings
    courses: list[str] = Field(..., description="List of Fenix course URLs to scrape.")
