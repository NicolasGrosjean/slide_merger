from typing import Self

from pydantic import model_validator
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    YamlConfigSettingsSource,
)


class ApiClientSettings(BaseSettings):
    """Settings of the client which call the backend API."""

    base_url: str = "http://localhost:8899"
    filenames_endpoint: str = "files/filenames"
    filename_timeout: int = 5

    @property
    def filenames_url(self) -> str:
        """Get the full URL of the filenames endpoint."""
        return f"{self.base_url}/{self.filenames_endpoint}"


class SlidePartSettings(BaseSettings):
    """Settings to choose the slide part to be used."""

    # Description of the slide part to know each slide to set
    description: str | None = None

    # Subdirectory where to look the slide files
    subdirectory: str

    # Filter the names in the subdirectory when show suggestions
    name_filter: str | None = None

    # Placeholder to be used if the wanted file is not found
    placeholder: str | None = None

    # Skip searching and use directly this file if provided
    file_name: str | None = None

    @model_validator(mode="after")
    def placeholder_or_file_name(self) -> Self:
        """Validate the settings."""
        if not self.placeholder and not self.file_name:
            err_msg = "SlidePartSettings: Either 'placeholder' or 'file_name' must be provided"
            raise ValueError(err_msg)
        return self


class Settings(BaseSettings):
    """Settings of the application."""

    model_config = SettingsConfigDict(
        yaml_file="settings.yaml",
        yaml_file_encoding="utf-8",
    )

    log_level: str = "INFO"
    max_file_suggestion_nb: int = 5
    api_client: ApiClientSettings = ApiClientSettings()
    slides: list[SlidePartSettings] = []

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """Customize the sources of the settings."""
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            file_secret_settings,
            YamlConfigSettingsSource(settings_cls),
        )
