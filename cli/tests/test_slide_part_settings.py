import pytest
import requests
import responses

from src.slide_part_settings import SlidePartSettings, SlidePartSettingsClient


def test_slidepartsettings_with_placeholder_but_no_filename() -> None:
    settings = SlidePartSettings(
        description="Test slide part",
        subdirectory="test_subdir",
        name_filter="test_filter",
        placeholder="test_placeholder",
    )
    assert settings.placeholder == "test_placeholder"
    assert settings.file_name is None


def test_slidepartsettings_with_filename_but_no_placeholder() -> None:
    settings = SlidePartSettings(
        description="Test slide part",
        subdirectory="test_subdir",
        name_filter="test_filter",
        file_name="test_file.txt",
    )
    assert settings.file_name == "test_file.txt"
    assert settings.placeholder is None


def test_slidepartsettings_with_neither_placeholder_nor_filename() -> None:
    with pytest.raises(ValueError, match="SlidePartSettings: Either 'placeholder' or 'file_name' must be provided"):
        SlidePartSettings(
            description="Test slide part",
            subdirectory="test_subdir",
            name_filter="test_filter",
        )


@responses.activate
def test_get_slide_part_settings_success() -> None:
    mock = responses.get(
        "http://example",
        status=200,
        json=[{"subdirectory": "slide_parts/part1", "name_filter": "part1", "placeholder": "placeholder"}],
    )
    fs = SlidePartSettingsClient("http://example", timeout=1)
    actual = fs.get_slide_part_settings()
    assert mock.call_count == 1
    assert len(actual) == 1
    assert actual[0].subdirectory == "slide_parts/part1"
    assert actual[0].name_filter == "part1"
    assert actual[0].placeholder == "placeholder"


@responses.activate
def test_get_slide_part_settings_error_returns_empty() -> None:
    mock = responses.get("http://example", status=500)
    fs = SlidePartSettingsClient("http://example", timeout=1)
    with pytest.raises(requests.exceptions.HTTPError):
        fs.get_slide_part_settings()
    assert mock.call_count == 1
