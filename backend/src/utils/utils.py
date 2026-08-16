import datetime
import sys
import time
from collections.abc import Callable
from typing import Any

from loguru import logger

STATUS_OK_HUNDRED = 2


def calculate_time_spent(function: Callable) -> Callable:
    """Execute a function and compute the time taken."""

    def wrapper(*args, **kwargs) -> Any:  # noqa: ANN002, ANN003, ANN401
        """Wrap to compute the time spent."""
        start = time.time()
        result = function(*args, **kwargs)
        end = time.time()
        logger.info(
            f"Total time of the execution of {function.__qualname__}: {datetime.timedelta(seconds=end - start)}"
        )
        return result

    return wrapper


def set_log_level(level: str) -> None:
    """Set the log level for the application."""
    logger.remove()
    logger.add(sys.stderr, level=level)
