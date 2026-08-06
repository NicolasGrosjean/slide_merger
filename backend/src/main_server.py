import uvicorn
from loguru import logger

import src
from src.webapi.container import BackendContainer
from src.webapi.webapi import create_webapi


def main() -> None:
    """Run the web api server."""
    container = BackendContainer()
    container.wire(packages=[src])

    settings = container.settings()
    logger.info(settings)  # TODO Improve with tabulate but make tabulate optional

    server = uvicorn.Server(
        uvicorn.Config(
            app=create_webapi(),
            host=settings.api.host,
            port=settings.api.port,
        )
    )
    server.run()


if __name__ == "__main__":
    main()
