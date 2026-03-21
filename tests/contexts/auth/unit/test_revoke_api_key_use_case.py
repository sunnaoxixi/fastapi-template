from uuid import uuid4

import pytest

from src.contexts.auth.application.use_cases.revoke_api_key import (
    RevokeApiKeyDTO,
    RevokeApiKeyUseCase,
)
from src.contexts.auth.domain.errors import ApiKeyNotFoundError, UserNotFoundError
from src.contexts.shared.infrastructure.events.in_memory_event_bus import (
    InMemoryEventBus,
)
from tests.contexts.auth.conftest import FakeUserRepository
from tests.support.factories import UserFactory


@pytest.mark.unit
class TestRevokeApiKeyUseCase:
    async def test_revokes_api_key(
        self,
        fake_user_repository: FakeUserRepository,
    ) -> None:
        user, plain_key = UserFactory.with_api_key()
        await fake_user_repository.save(user)
        event_bus = InMemoryEventBus()
        use_case = RevokeApiKeyUseCase(fake_user_repository, event_bus)

        await use_case.execute(RevokeApiKeyDTO(user_id=user.user_id, api_key=plain_key))

        saved_user = await fake_user_repository.find_by_id(user.user_id)
        assert saved_user is not None
        assert saved_user.api_keys[0].is_active is False

    async def test_raises_error_for_nonexistent_user(
        self, fake_user_repository: FakeUserRepository
    ) -> None:
        event_bus = InMemoryEventBus()
        use_case = RevokeApiKeyUseCase(fake_user_repository, event_bus)

        with pytest.raises(UserNotFoundError):
            await use_case.execute(RevokeApiKeyDTO(user_id=uuid4(), api_key="any"))

    async def test_raises_error_for_nonexistent_api_key(
        self, fake_user_repository: FakeUserRepository
    ) -> None:
        user = UserFactory.build()
        await fake_user_repository.save(user)
        event_bus = InMemoryEventBus()
        use_case = RevokeApiKeyUseCase(fake_user_repository, event_bus)

        with pytest.raises(ApiKeyNotFoundError):
            await use_case.execute(
                RevokeApiKeyDTO(user_id=user.user_id, api_key="nonexistent")
            )
