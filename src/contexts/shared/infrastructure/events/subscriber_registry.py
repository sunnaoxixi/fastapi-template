from src.contexts.auth.domain.events import (
    ApiKeyCreatedEvent,
    ApiKeyRevokedEvent,
    UserCreatedEvent,
)
from src.contexts.shared.domain.events import DomainEvent, EventBus, EventHandler
from src.contexts.shared.infrastructure.events.logging_subscriber import (
    log_domain_event,
)

SUBSCRIPTIONS: list[tuple[type[DomainEvent], EventHandler]] = [
    (UserCreatedEvent, log_domain_event),
    (ApiKeyCreatedEvent, log_domain_event),
    (ApiKeyRevokedEvent, log_domain_event),
]


def register_event_subscribers(event_bus: EventBus) -> None:
    for event_type, handler in SUBSCRIPTIONS:
        event_bus.subscribe(event_type, handler)
