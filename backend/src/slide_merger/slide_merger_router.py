from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from src.slide_merger.slide_merger_service import SlideMergerService
from src.webapi.container import BackendContainer
from src.webapi.settings import Settings, SlidePartSettings

router = APIRouter()


class MergeSlidesRequest(BaseModel):
    """Request model for merging slides."""

    input_slides: list[str] = Field(min_length=1)
    output_file_name: str = Field(min_length=1)


@router.get("/config", response_model=list[SlidePartSettings])
@inject
def slide_parts_config(
    settings: Annotated[Settings, Depends(Provide[BackendContainer.settings])],
) -> list[SlidePartSettings]:
    """Return the configured slide parts used by the CLI and web UI."""
    return settings.slides


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
