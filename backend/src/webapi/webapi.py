from typing import TYPE_CHECKING

from dependency_injector.wiring import Provide, inject
from fastapi import FastAPI, Request, status
from fastapi.concurrency import asynccontextmanager
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from loguru import logger

from src.files.files_router import router as files_router
from src.slide_merger.slide_merger_router import router as slide_merger_router
from src.utils.utils import set_log_level
from src.webapi.container import BackendContainer
from src.webapi.settings import Settings

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator


@inject
def create_webapi(
    settings: Settings = Provide[BackendContainer.settings],
) -> FastAPI:
    """Create Web API."""
    webapi = _init_webapi(
        settings,
        title="Slide Merger API",
        description="API for merging slides",
    )
    webapi.include_router(slide_merger_router, prefix="/slide_merger")
    webapi.include_router(files_router, prefix="/files")

    @webapi.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):  # noqa: ANN202
        exc_str = f"{exc}".replace("\n", " ").replace("   ", " ")
        logger.error(f"{request}: {exc_str}")
        content = {"status_code": 10422, "message": exc_str, "data": None}
        return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

    return webapi


def _init_webapi(
    settings: Settings,
    title: str,
    description: str,
) -> FastAPI:
    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncGenerator[None]:
        set_log_level(settings.log_level)
        logger.info("FastAPI app started")
        yield
        logger.info("FastAPI app shutdown")

    return FastAPI(
        title=title,
        description=description,
        lifespan=lifespan,
        openapi_url="/api/v0/openapi.json" if not settings.api.hide_fastapi_docs else None,
        docs_url="/api/v0/docs" if not settings.api.hide_fastapi_docs else None,
        redoc_url="/api/v0/redoc" if not settings.api.hide_fastapi_docs else None,
    )
