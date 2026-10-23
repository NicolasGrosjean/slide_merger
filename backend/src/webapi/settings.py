from pathlib import Path
from typing import Self

from pydantic import model_validator
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    YamlConfigSettingsSource,
)


class ApiSettings(BaseSettings):
    """Settings of the API."""

    host: str = "localhost"
    port: int = 8899
    hide_fastapi_docs: bool = False
    cors_origins: list[str] = ["http://localhost:4200"]


class SlidePartSettings(BaseSettings):
    """Configuration required to render one slide selector."""

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
    api: ApiSettings = ApiSettings()
    root_data_directory: Path = Path()
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
