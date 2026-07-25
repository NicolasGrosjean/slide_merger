from pathlib import Path
from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from src.slide_merger.slide_merger_service import SlideMergerService
from src.webapi.container import BackendContainer

router = APIRouter()


class MergeSlidesRequest(BaseModel):
    """Request model for merging slides."""

    input_slides: list[Path]
    output_path: Path


@router.post("/merge")
@inject
def merge_slides(
    request: MergeSlidesRequest,
    slide_merger_service: Annotated[SlideMergerService, Depends(Provide[BackendContainer.slide_merger_service])],
) -> None:
    """Merge slides from the input PowerPoint presentations into a single presentation."""
    return slide_merger_service.merge(request.input_slides, request.output_path)
