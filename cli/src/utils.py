import json
import sys

import requests
from loguru import logger

STATUS_OK_HUNDRED = 2


def manage_request_error(r: requests.models.Response) -> None:
    """Manage request error by logging the error message and raise HTTPError."""
    if r.status_code // 100 != STATUS_OK_HUNDRED:
        try:
            content = r._content.decode() if r._content is not None else ""  # noqa: SLF001
            error = json.loads(content)
        except json.decoder.JSONDecodeError:
            msg = f"{r.status_code}: {r._content.decode() if r._content is not None else ''}"  # noqa: SLF001
            logger.error(msg)
            r.raise_for_status()
        if "message" in error:
            logger.error(error["message"])
        elif "detail" in error:
            logger.error(error["detail"])
        else:
            logger.error(error)
        r.raise_for_status()


def set_log_level(level: str) -> None:
    """Set the log level for the application."""
    logger.remove()
    logger.add(sys.stderr, level=level)
