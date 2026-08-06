import pytest

from src.settings import SlidePartSettings


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
