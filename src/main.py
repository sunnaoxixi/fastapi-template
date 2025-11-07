from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from loguru import logger

from src.container import ApplicationContainer
from src.contexts.auth.infrastructure.http import auth_router, verify_api_key
from src.contexts.shared.infrastructure.http import public
from src.contexts.shared.infrastructure.logger import setup_logger

container = ApplicationContainer()


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    container.wire(
        modules=[
            "src.contexts.auth.infrastructure.http.routes",
            "src.contexts.auth.infrastructure.http.api_key_middleware",
        ]
    )

    try:
        yield
    finally:
        await container.unwire()
        logger.complete()


app = FastAPI(
    title="FastAPI Template",
    description=(
        "A FastAPI template with DDD, Clean Architecture, and Dependency Injection"
    ),
    version="1.0.0",
    lifespan=lifespan,
    dependencies=[Depends(verify_api_key)],
)

setup_logger(app)

app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])


@app.get("/health", tags=["Health"])
@public
def read_health() -> dict[str, str]:
    return {"status": "healthy"}
