import pytest

from src.contexts.auth.application.use_cases.create_user import (
    CreateUserDTO,
    CreateUserUseCase,
)
from src.contexts.auth.domain.errors import UsernameAlreadyExistsError
from src.contexts.shared.infrastructure.events.in_memory_event_bus import (
    InMemoryEventBus,
)
from tests.contexts.auth.conftest import FakeUserRepository


@pytest.mark.unit
class TestCreateUserUseCase:
    async def test_creates_user_with_hashed_password(
        self, fake_user_repository: FakeUserRepository
    ) -> None:
        event_bus = InMemoryEventBus()
        use_case = CreateUserUseCase(fake_user_repository, event_bus)

        user = await use_case.execute(
            CreateUserDTO(username="newuser", password="password123")
        )

        assert user.username == "newuser"
        assert user.password.startswith("$2b$")
        assert fake_user_repository.count() == 1

    async def test_raises_error_for_duplicate_username(
        self, fake_user_repository: FakeUserRepository
    ) -> None:
        event_bus = InMemoryEventBus()
        use_case = CreateUserUseCase(fake_user_repository, event_bus)

        await use_case.execute(
            CreateUserDTO(username="duplicate", password="password123")
        )

        with pytest.raises(UsernameAlreadyExistsError):
            await use_case.execute(
                CreateUserDTO(username="duplicate", password="password456")
            )
