from dependency_injector import containers, providers

from src.slide_merger.slide_merger_service import SlideMergerService
from src.webapi.settings import Settings


class BackendContainer(containers.DeclarativeContainer):
    """Dependency injection container for the application."""

    settings = providers.Singleton(lambda: Settings())

    slide_merger_service = providers.Singleton(lambda: SlideMergerService())
