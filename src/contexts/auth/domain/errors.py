from uuid import UUID

from src.contexts.shared.domain.errors import (
    ForbiddenError,
    NotFoundError,
    UnauthorizedError,
)


class MissingApiKeyError(UnauthorizedError):
    def __init__(self) -> None:
        super().__init__("API key is required.")


class InvalidApiKeyError(UnauthorizedError):
    def __init__(self) -> None:
        super().__init__("The provided API key is invalid.")


class InactiveApiKeyError(ForbiddenError):
    def __init__(self, message: str = "The provided API key is inactive.") -> None:
        super().__init__(message)


class UserNotFoundError(NotFoundError):
    def __init__(self, user_id: UUID) -> None:
        super().__init__(f"User with id {user_id} not found")
        self.user_id = user_id


class ApiKeyNotFoundError(NotFoundError):
    def __init__(self, api_key: str | None = None) -> None:
        super().__init__(
            f"API key not found: {api_key}" if api_key else "API key not found"
        )
        self.api_key = api_key
