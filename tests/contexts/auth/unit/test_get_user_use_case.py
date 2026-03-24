from uuid import uuid4

import pytest

from src.contexts.auth.application.use_cases.get_user import (
    GetUserDTO,
    GetUserUseCase,
)
from src.contexts.auth.domain.errors import UserNotFoundError
from tests.contexts.auth.conftest import FakeUserRepository
from tests.support.factories import UserFactory


@pytest.mark.unit
class TestGetUserUseCase:
    async def test_returns_user_by_id(
        self,
        fake_user_repository: FakeUserRepository,
    ) -> None:
        user = UserFactory.build()
        await fake_user_repository.save(user)
        use_case = GetUserUseCase(fake_user_repository)

        result = await use_case.execute(GetUserDTO(user_id=user.user_id))

        assert result.user_id == user.user_id
        assert result.username == user.username

    async def test_raises_error_for_nonexistent_user(
        self, fake_user_repository: FakeUserRepository
    ) -> None:
        use_case = GetUserUseCase(fake_user_repository)

        with pytest.raises(UserNotFoundError):
            await use_case.execute(GetUserDTO(user_id=uuid4()))
