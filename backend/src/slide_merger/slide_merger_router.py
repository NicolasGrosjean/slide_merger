from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from src.slide_merger.slide_merger_service import SlideMergerService
from src.webapi.container import BackendContainer
from src.webapi.settings import Settings

router = APIRouter()


class MergeSlidesRequest(BaseModel):
    """Request model for merging slides."""

    input_slides: list[str]
    output_file_name: str


@router.post("/merge")
@inject
def merge_slides(
    request: MergeSlidesRequest,
    settings: Annotated[Settings, Depends(Provide[BackendContainer.settings])],
    slide_merger_service: Annotated[SlideMergerService, Depends(Provide[BackendContainer.slide_merger_service])],
) -> None:
    """Merge slides from the input PowerPoint presentations into a single presentation."""
    return slide_merger_service.merge(
        [settings.root_data_directory / slide for slide in request.input_slides],
        settings.root_data_directory / request.output_file_name,
    )
