from pydantic import BaseModel, PrivateAttr

from src.contexts.shared.domain.events import DomainEvent


class AggregateRoot(BaseModel):
    model_config = {"populate_by_name": True}

    _events: list[DomainEvent] = PrivateAttr(default_factory=list)

    def record_event(self, event: DomainEvent) -> None:
        self._events.append(event)

    def pull_events(self) -> list[DomainEvent]:
        events = list(self._events)
        self._events.clear()
        return events
