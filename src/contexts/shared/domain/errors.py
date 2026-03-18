class DomainError(Exception):
    """Base class for all domain errors."""


class NotFoundError(DomainError):
    """Raised when a requested entity does not exist."""


class ConflictError(DomainError):
    """Raised when an operation conflicts with the current state."""


class ForbiddenError(DomainError):
    """Raised when an operation is not permitted."""


class UnauthorizedError(DomainError):
    """Raised when authentication fails."""
