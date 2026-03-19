from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CursorParams:
    cursor: str | None = None
    page_size: int = 20


@dataclass(frozen=True, slots=True)
class CursorResult[T]:
    items: list[T]
    next_cursor: str | None
    previous_cursor: str | None
