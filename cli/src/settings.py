import os
from typing import Self

from pydantic import Field, model_validator
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    YamlConfigSettingsSource,
)


class ApiClientSettings(BaseSettings):
    """Settings of the client which call the backend API."""

    model_config = SettingsConfigDict(env_prefix="API_")

    base_url: str = "http://localhost:8899"
    filenames_endpoint: str = "files/filenames"
    filename_timeout: int = 5
    slide_merge_endpoint: str = "slide_merger/merge"
    slide_merge_timeout: int = 60

    def model_post_init(self, __context) -> None:  # noqa
        """Allow environment variables to override values from YAML."""
        # TODO Fix sttings to remove this method and use the env_prefix of pydantic-settings instead.

        # Check for environment variables and override if they exist
        if "API_BASE_URL" in os.environ:
            self.base_url = os.environ["API_BASE_URL"]
        if "API_FILENAMES_ENDPOINT" in os.environ:
            self.filenames_endpoint = os.environ["API_FILENAMES_ENDPOINT"]
        if "API_FILENAME_TIMEOUT" in os.environ:
            self.filename_timeout = int(os.environ["API_FILENAME_TIMEOUT"])
        if "API_SLIDE_MERGE_ENDPOINT" in os.environ:
            self.slide_merge_endpoint = os.environ["API_SLIDE_MERGE_ENDPOINT"]
        if "API_SLIDE_MERGE_TIMEOUT" in os.environ:
            self.slide_merge_timeout = int(os.environ["API_SLIDE_MERGE_TIMEOUT"])

    @property
    def filenames_url(self) -> str:
        """Get the full URL of the filenames endpoint."""
        return f"{self.base_url}/{self.filenames_endpoint}"

    @property
    def slide_merge_url(self) -> str:
        """Get the full URL of the slide merge endpoint."""
        return f"{self.base_url}/{self.slide_merge_endpoint}"


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

    model_config = SettingsConfigDict(yaml_file="settings.yaml", yaml_file_encoding="utf-8")

    log_level: str = "INFO"
    max_file_suggestion_nb: int = 5
    api_client: ApiClientSettings = Field(default_factory=ApiClientSettings)
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
