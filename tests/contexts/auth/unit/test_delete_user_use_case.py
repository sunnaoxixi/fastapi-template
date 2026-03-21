from uuid import uuid4

import pytest

from src.contexts.auth.application.use_cases.delete_user import (
    DeleteUserDTO,
    DeleteUserUseCase,
)
from src.contexts.auth.domain.errors import UserNotFoundError
from tests.contexts.auth.conftest import FakeUserRepository
from tests.support.factories import UserFactory


@pytest.mark.unit
class TestDeleteUserUseCase:
    async def test_deletes_existing_user(
        self,
        fake_user_repository: FakeUserRepository,
    ) -> None:
        user = UserFactory.build()
        await fake_user_repository.save(user)
        use_case = DeleteUserUseCase(fake_user_repository)

        await use_case.execute(DeleteUserDTO(user_id=user.user_id))

        assert fake_user_repository.count() == 0

    async def test_raises_error_for_nonexistent_user(
        self, fake_user_repository: FakeUserRepository
    ) -> None:
        use_case = DeleteUserUseCase(fake_user_repository)

        with pytest.raises(UserNotFoundError):
            await use_case.execute(DeleteUserDTO(user_id=uuid4()))
