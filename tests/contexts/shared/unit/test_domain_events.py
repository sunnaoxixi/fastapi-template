from dataclasses import dataclass

import pytest

from src.contexts.shared.domain.aggregate_root import AggregateRoot
from src.contexts.shared.domain.events import DomainEvent


@dataclass(frozen=True, slots=True)
class UserCreated(DomainEvent):
    user_id: str


@dataclass(frozen=True, slots=True)
class UserDeleted(DomainEvent):
    user_id: str


class DummyAggregate(AggregateRoot):
    name: str

    def do_something(self) -> None:
        self.record_event(UserCreated(user_id="abc"))


@pytest.mark.unit
class TestAggregateRootEvents:
    def test_new_aggregate_has_no_events(self) -> None:
        aggregate = DummyAggregate(name="test")

        assert aggregate.pull_events() == []

    def test_record_and_pull_returns_events(self) -> None:
        aggregate = DummyAggregate(name="test")
        event = UserCreated(user_id="abc")

        aggregate.record_event(event)

        assert aggregate.pull_events() == [event]

    def test_pull_clears_the_event_list(self) -> None:
        aggregate = DummyAggregate(name="test")
        aggregate.record_event(UserCreated(user_id="abc"))

        aggregate.pull_events()

        assert aggregate.pull_events() == []

    def test_multiple_events_preserve_order(self) -> None:
        aggregate = DummyAggregate(name="test")
        first = UserCreated(user_id="first")
        second = UserDeleted(user_id="second")
        third = UserCreated(user_id="third")

        aggregate.record_event(first)
        aggregate.record_event(second)
        aggregate.record_event(third)

        assert aggregate.pull_events() == [first, second, third]
