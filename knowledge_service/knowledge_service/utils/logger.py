"""
Logging utilities for integrating standard logging with Loguru.

This module provides an InterceptHandler to redirect standard logging records to Loguru,
and a setup_logger function to configure logging with a Spring Boot-like format.
"""

import inspect
import logging
import sys

from knowledge_service.utils.settings import Settings
from loguru import logger


class InterceptHandler(logging.Handler):
    """A logging handler that intercepts standard logging records and redirects them to Loguru."""

    def emit(self, record: logging.LogRecord) -> None:
        """
        Emit a logging record by redirecting it to Loguru.

        Args:
            record (logging.LogRecord): The log record to be processed.

        """
        # Get corresponding Loguru level if it exists.
        try:
            level: str | int = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message.
        frame, depth = inspect.currentframe(), 0
        while frame:
            filename = frame.f_code.co_filename
            is_logging = filename == logging.__file__
            is_frozen = "importlib" in filename and "_bootstrap" in filename
            if depth > 0 and not (is_logging or is_frozen):
                break
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def setup_logger(settings: Settings) -> None:
    """
    Set up logging configuration for the application using Loguru and standard logging.

    Args:
        settings (Settings): The application settings containing the log level.

    """
    # Remove all existing handlers
    logger.remove()

    # Add Loguru handler with your preferred format
    log_format = (
        "{time:YYYY-MM-DD HH:mm:ss.SSS}  {level: <5} {process} --- [{thread.name}] {name}.{function}:{line} : {message}"
    )
    logger.add(
        sys.stderr,
        format=log_format,
        level=settings.log_level,
        colorize=False,
    )

    # Patch root logger
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

    # Patch Uvicorn loggers
    for uvicorn_logger_key in ("uvicorn", "uvicorn.error", "uvicorn.access"):
        uvicorn_logger = logging.getLogger(uvicorn_logger_key)
        uvicorn_logger.handlers = [InterceptHandler()]
        uvicorn_logger.propagate = False
