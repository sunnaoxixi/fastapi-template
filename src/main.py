from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

from src.container import ApplicationContainer
from src.contexts.shared.infrastructure.logger import setup_logger


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    container = ApplicationContainer()
    container.wire(modules=[__name__])

    try:
        yield
    finally:
        logger.complete()


app = FastAPI(lifespan=lifespan)

setup_logger(app)


@app.get("/health")
def read_health() -> dict:
    return {"status": "healthy"}
