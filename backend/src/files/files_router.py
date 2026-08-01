from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from src.files.files_service import FilesService
from src.webapi.container import BackendContainer
from src.webapi.settings import Settings

router = APIRouter()


class FilesRequest(BaseModel):
    """Request model for getting available file names."""

    sub_directory: str
    filter: str | None = None


@router.get("/filenames")
@inject
def available_file_names(
    request: FilesRequest,
    settings: Annotated[Settings, Depends(Provide[BackendContainer.settings])],
    files_service: Annotated[FilesService, Depends(Provide[BackendContainer.files_service])],
) -> list[str]:
    """Get the names of available files."""
    return files_service.get_available_file_names(settings.root_data_directory, request.sub_directory, request.filter)
