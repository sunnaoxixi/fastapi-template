import pytest
from fastapi import Request

from src.contexts.shared.domain.errors import (
    ConflictError,
    DomainError,
    ForbiddenError,
    NotFoundError,
    UnauthorizedError,
)
from src.contexts.shared.infrastructure.http.exception_handlers import (
    domain_error_handler,
)


@pytest.mark.unit
class TestDomainErrorHandler:
    @pytest.fixture
    def mock_request(self) -> Request:
        return Request(scope={"type": "http", "method": "GET", "path": "/"})

    async def test_not_found_error_returns_404(self, mock_request: Request) -> None:
        exc = NotFoundError("Thing not found")

        response = await domain_error_handler(mock_request, exc)

        assert response.status_code == 404
        assert response.body == b'{"detail":"Thing not found"}'

    async def test_conflict_error_returns_409(self, mock_request: Request) -> None:
        exc = ConflictError("Already exists")

        response = await domain_error_handler(mock_request, exc)

        assert response.status_code == 409
        assert response.body == b'{"detail":"Already exists"}'

    async def test_forbidden_error_returns_403(self, mock_request: Request) -> None:
        exc = ForbiddenError("Not allowed")

        response = await domain_error_handler(mock_request, exc)

        assert response.status_code == 403
        assert response.body == b'{"detail":"Not allowed"}'

    async def test_unauthorized_error_returns_401(self, mock_request: Request) -> None:
        exc = UnauthorizedError("Bad credentials")

        response = await domain_error_handler(mock_request, exc)

        assert response.status_code == 401
        assert response.body == b'{"detail":"Bad credentials"}'

    async def test_bare_domain_error_returns_400(self, mock_request: Request) -> None:
        exc = DomainError("Something went wrong")

        response = await domain_error_handler(mock_request, exc)

        assert response.status_code == 400
        assert response.body == b'{"detail":"Something went wrong"}'

    async def test_not_found_subclass_returns_404(self, mock_request: Request) -> None:
        class ItemNotFoundError(NotFoundError):
            pass

        exc = ItemNotFoundError("Item gone")

        response = await domain_error_handler(mock_request, exc)

        assert response.status_code == 404
        assert response.body == b'{"detail":"Item gone"}'
