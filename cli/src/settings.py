import os

from pydantic import Field
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
    config_endpoint: str = "slide_merger/config"
    config_timeout: int = 5
    filenames_endpoint: str = "files/filenames"
    filename_timeout: int = 5
    slide_merge_endpoint: str = "slide_merger/merge"
    slide_merge_timeout: int = 60

    def model_post_init(self, __context) -> None:  # noqa
        """Allow environment variables to override values from YAML."""
        # TODO Fix settings to remove this method and use the env_prefix of pydantic-settings instead.

        # Check for environment variables and override if they exist
        if "API_BASE_URL" in os.environ:
            self.base_url = os.environ["API_BASE_URL"]
        if "API_CONFIG_ENDPOINT" in os.environ:
            self.config_endpoint = os.environ["API_CONFIG_ENDPOINT"]
        if "API_CONFIG_TIMEOUT" in os.environ:
            self.config_timeout = int(os.environ["API_CONFIG_TIMEOUT"])
        if "API_FILENAMES_ENDPOINT" in os.environ:
            self.filenames_endpoint = os.environ["API_FILENAMES_ENDPOINT"]
        if "API_FILENAME_TIMEOUT" in os.environ:
            self.filename_timeout = int(os.environ["API_FILENAME_TIMEOUT"])
        if "API_SLIDE_MERGE_ENDPOINT" in os.environ:
            self.slide_merge_endpoint = os.environ["API_SLIDE_MERGE_ENDPOINT"]
        if "API_SLIDE_MERGE_TIMEOUT" in os.environ:
            self.slide_merge_timeout = int(os.environ["API_SLIDE_MERGE_TIMEOUT"])

    @property
    def config_url(self) -> str:
        """Get the full URL of the config endpoint."""
        return f"{self.base_url}/{self.config_endpoint}"

    @property
    def filenames_url(self) -> str:
        """Get the full URL of the filenames endpoint."""
        return f"{self.base_url}/{self.filenames_endpoint}"

    @property
    def slide_merge_url(self) -> str:
        """Get the full URL of the slide merge endpoint."""
        return f"{self.base_url}/{self.slide_merge_endpoint}"


class Settings(BaseSettings):
    """Settings of the application."""

    model_config = SettingsConfigDict(yaml_file="settings.yaml", yaml_file_encoding="utf-8")

    log_level: str = "INFO"
    max_file_suggestion_nb: int = 5
    api_client: ApiClientSettings = Field(default_factory=ApiClientSettings)

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
