from typing import Self

import requests
from pydantic import model_validator
from pydantic_settings import BaseSettings

from src.utils import manage_request_error


class SlidePartSettingsClient:
    """Class to get slide part settings."""

    def __init__(self, slide_part_settings_url: str, timeout: int):
        self.slide_part_settings_url = slide_part_settings_url
        self.timeout = timeout

    def get_slide_part_settings(self) -> list[SlidePartSettings]:
        """Get the slide part settings from the backend API."""
        r = requests.get(self.slide_part_settings_url, timeout=self.timeout)
        manage_request_error(r)
        return [SlidePartSettings(**slide_part) for slide_part in r.json()]


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
