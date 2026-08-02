from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Query

from src.files.files_service import FilesService
from src.webapi.container import BackendContainer
from src.webapi.settings import Settings

router = APIRouter()


@router.get("/filenames")
@inject
def available_file_names(
    sub_directory: Annotated[str, Query()],
    settings: Annotated[Settings, Depends(Provide[BackendContainer.settings])],
    files_service: Annotated[FilesService, Depends(Provide[BackendContainer.files_service])],
    name_filter: Annotated[str | None, Query()] = None,
) -> list[str]:
    """Get the names of available files."""
    try:
        return files_service.get_available_file_names(settings.root_data_directory, sub_directory, name_filter)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
