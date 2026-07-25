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


class Settings(BaseSettings):
    """Settings of the application."""

    model_config = SettingsConfigDict(
        yaml_file="settings.yaml",
        yaml_file_encoding="utf-8",
    )

    log_level: str = "INFO"
    api: ApiSettings = ApiSettings()

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
