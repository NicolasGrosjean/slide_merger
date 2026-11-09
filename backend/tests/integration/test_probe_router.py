from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from src.webapi.settings import Settings, SlidePartSettings


def test_ready_probe_returns_true_when_configured_paths_exist(settings: Settings, client: TestClient) -> None:
    slides_directory = settings.root_data_directory / "slides"
    slides_directory.mkdir()
    (slides_directory / "fixed.pptx").touch()
    (settings.root_data_directory / "placeholder.pptx").touch()
    settings.slides = [
        SlidePartSettings(subdirectory="slides", file_name="fixed.pptx"),
        SlidePartSettings(subdirectory="slides", placeholder="placeholder.pptx"),
    ]

    response = client.get("/ready")

    assert response.status_code == 200
    assert response.json() is True


def test_ready_probe_raises_when_root_data_directory_is_missing(
    settings: Settings, client: TestClient, tmp_path: Path
) -> None:
    missing_root = tmp_path / "missing"
    settings.root_data_directory = missing_root

    with pytest.raises(RuntimeError, match=f"Root data directory does not exist: {missing_root}"):
        client.get("/ready")


def test_ready_probe_reports_missing_configured_paths(settings: Settings, client: TestClient) -> None:
    settings.slides = [
        SlidePartSettings(subdirectory="missing-slides", file_name="missing.pptx"),
        SlidePartSettings(subdirectory="missing-placeholder", placeholder="placeholder.pptx"),
    ]

    with pytest.raises(RuntimeError) as exc_info:
        client.get("/ready")

    assert str(exc_info.value).splitlines() == [
        f"Subdirectory does not exist: {settings.root_data_directory / 'missing-slides'}",
        f"File does not exist: {settings.root_data_directory / 'missing-slides' / 'missing.pptx'}",
        f"Subdirectory does not exist: {settings.root_data_directory / 'missing-placeholder'}",
        f"Placeholder does not exist: {settings.root_data_directory / 'placeholder.pptx'}",
    ]
