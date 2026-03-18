from abc import ABC, abstractmethod
from collections.abc import Callable, Coroutine
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass(frozen=True, slots=True)
class DomainEvent:
    occurred_on: datetime = field(default_factory=lambda: datetime.now(UTC), kw_only=True)


EventHandler = Callable[[DomainEvent], Coroutine[Any, Any, None]]


class EventBus(ABC):
    @abstractmethod
    async def publish(self, events: list[DomainEvent]) -> None: ...

    @abstractmethod
    def subscribe(self, event_type: type[DomainEvent], handler: EventHandler) -> None: ...
