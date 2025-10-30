import logging
import sys

from fastapi import FastAPI
from loguru import logger

from src.settings import settings

from .middleware import (
    log_requests,
    log_requests_development,
)


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def configure_loguru(
    logger_names: list[str] | None = None,
    *,
    backtrace: bool = True,
    diagnose: bool = True,
    enqueue: bool = True,
) -> None:
    if logger_names is None:
        for logger_name in logging.root.manager.loggerDict:
            logging_logger = logging.getLogger(logger_name)
            logging_logger.handlers = []
            logging_logger.propagate = True
        logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO)
    else:
        for logger_name in logger_names:
            logging_logger = logging.getLogger(logger_name)
            logging_logger.handlers = [InterceptHandler()]
            logging_logger.propagate = False

    logger.remove()
    logger.add(
        sys.stdout,
        level=settings.log_level,
        colorize=True,
        backtrace=backtrace,
        diagnose=diagnose,
        enqueue=enqueue,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level}</level> | "
            "<magenta>{module}</magenta> | "
            "<level>{message}</level>"
        ),
    )


def setup_logger(app: FastAPI) -> None:
    configure_loguru()

    if settings.is_development:
        app.middleware("http")(log_requests_development)
    else:
        app.middleware("http")(log_requests)
