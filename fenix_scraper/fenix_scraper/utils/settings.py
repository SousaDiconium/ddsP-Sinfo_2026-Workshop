"""Defines the settings for the knowledge service application."""

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource, SettingsConfigDict, YamlConfigSettingsSource

current_path = Path(__file__)
resources_path = current_path.parent.parent / "resources"


class SubjectSubPageSettings(BaseSettings):
    """Settings for a specific subject sub-page within a course."""

    name: str = Field(..., description="The name of the subject sub-page (e.g., 'initial-page', 'announcements').")
    url_suffix: str = Field(
        ..., description="The URL suffix for the subject sub-page (e.g., '/pagina-inicial', '/anuncios')."
    )
    blacklisted_attachments: list[str] = Field(
        default_factory=list,
        description="List of attachment urls that should be ignored when scraping this sub-page.",
    )


class SubjectSettings(BaseSettings):
    """Settings for a specific subject within a course."""

    subject_url: str = Field(..., description="The URL of the Fenix subject page to scrape.")
    sub_pages: list[SubjectSubPageSettings] = Field(..., description="List of sub-pages within the subject.")


class CourseSettings(BaseSettings):
    """Settings for a specific course."""

    course_url: str = Field(..., description="The URL of the Fenix course page to scrape.")
    subjects: list[SubjectSettings] = Field(..., description="List of subjects within the course.")


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
    courses: list[CourseSettings] = Field(
        ..., description="List of courses to scrape, each with its own URL and subjects."
    )

    # Secrets
    jsession_id: str = Field(..., description="The JSESSIONID cookie value for authenticating with Fenix.")
