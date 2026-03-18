from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.contexts.shared.domain.errors import (
    ConflictError,
    DomainError,
    ForbiddenError,
    NotFoundError,
    UnauthorizedError,
)

ERROR_STATUS_MAP: dict[type[DomainError], int] = {
    NotFoundError: 404,
    ConflictError: 409,
    ForbiddenError: 403,
    UnauthorizedError: 401,
}

DEFAULT_STATUS_CODE = 400


async def domain_error_handler(_request: Request, exc: DomainError) -> JSONResponse:
    # Iteration order matters: first match wins via isinstance (subclass-aware).
    # If an error could match multiple base types, place the more specific one first.
    status_code = DEFAULT_STATUS_CODE
    for error_type, code in ERROR_STATUS_MAP.items():
        if isinstance(exc, error_type):
            status_code = code
            break
    return JSONResponse(status_code=status_code, content={"detail": str(exc)})


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(DomainError, domain_error_handler)
