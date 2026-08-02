from pathlib import Path

import pytest
from fastapi.testclient import TestClient

import src
from src.webapi.container import BackendContainer
from src.webapi.settings import Settings
from src.webapi.webapi import create_webapi


@pytest.fixture
def settings(tmp_path: Path) -> Settings:
    return Settings(log_level="DEBUG", root_data_directory=tmp_path)


@pytest.fixture
def client(settings: Settings) -> TestClient:
    container = BackendContainer()
    container.settings.override(settings)
    container.wire(packages=[src])
    return TestClient(create_webapi())
