from dependency_injector import containers, providers

from src.files.files_service import FilesService
from src.slide_merger.slide_merger_service import SlideMergerService
from src.webapi.settings import Settings


class BackendContainer(containers.DeclarativeContainer):
    """Dependency injection container for the application."""

    settings = providers.Singleton(Settings)

    files_service = providers.Singleton(FilesService)
    slide_merger_service = providers.Singleton(SlideMergerService)
