from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from loguru import logger

from src.webapi.container import BackendContainer
from src.webapi.settings import Settings

router = APIRouter()


@router.get("/ready")
@inject
async def health_check(
    settings: Annotated[Settings, Depends(Provide[BackendContainer.settings])],
) -> bool:
    """Check if the application is ready to serve requests by having access the data root directory."""
    if not settings.root_data_directory.exists():
        err_msg = f"Root data directory does not exist: {settings.root_data_directory}"
        logger.error(err_msg)
        raise RuntimeError(err_msg)
    err_messages = []
    for slide_part in settings.slides:
        subdirectory_path = settings.root_data_directory / slide_part.subdirectory
        if not subdirectory_path.exists():
            err_messages.append(f"Subdirectory does not exist: {subdirectory_path}")
        if slide_part.file_name:
            file_path = subdirectory_path / slide_part.file_name
            if not file_path.exists():
                err_messages.append(f"File does not exist: {file_path}")
        if slide_part.placeholder:
            placeholder_path = settings.root_data_directory / slide_part.placeholder
            if not placeholder_path.exists():
                err_messages.append(f"Placeholder does not exist: {placeholder_path}")
    if err_messages:
        err_msg = "\n".join(err_messages)
        logger.error(err_msg)
        raise RuntimeError(err_msg)
    return True


@router.get("/ping")
@inject
async def ping() -> bool:
    """Check if the application is alive."""
    return True
