import base64
from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import UUID

from src.contexts.shared.domain.errors import InvalidCursorError

_VALID_DIRECTIONS = {"next", "previous"}


def encode_cursor(direction: str, created_at: datetime, entity_id: UUID) -> str:
    raw = f"{direction}|{created_at.isoformat()}|{entity_id}"
    return base64.b64encode(raw.encode()).decode()


def decode_cursor(cursor: str) -> tuple[str, datetime, UUID]:
    try:
        raw = base64.b64decode(cursor.encode()).decode()
    except Exception as exc:
        raise InvalidCursorError("Cursor is not valid base64") from exc

    parts = raw.split("|")
    if len(parts) != 3:
        raise InvalidCursorError("Cursor has unexpected format")

    direction, raw_dt, raw_id = parts

    if direction not in _VALID_DIRECTIONS:
        raise InvalidCursorError(f"Unknown cursor direction: {direction!r}")

    try:
        created_at = datetime.fromisoformat(raw_dt)
    except ValueError as exc:
        raise InvalidCursorError("Cursor datetime is invalid") from exc

    if created_at.tzinfo is None:
        created_at = created_at.replace(tzinfo=UTC)

    try:
        entity_id = UUID(raw_id)
    except ValueError as exc:
        raise InvalidCursorError("Cursor entity ID is not a valid UUID") from exc

    return direction, created_at, entity_id


@dataclass(frozen=True, slots=True)
class CursorParams:
    cursor: str | None = None
    page_size: int = 20

    def __post_init__(self) -> None:
        if not (1 <= self.page_size <= 100):
            raise ValueError(f"page_size must be between 1 and 100, got {self.page_size}")


@dataclass(frozen=True, slots=True)
class CursorResult[T]:
    items: list[T]
    next_cursor: str | None
    previous_cursor: str | None
