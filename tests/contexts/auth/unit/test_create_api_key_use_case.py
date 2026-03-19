from uuid import uuid4

import pytest

from src.contexts.auth.application.use_cases.create_api_key import (
    CreateApiKeyDTO,
    CreateApiKeyUseCase,
)
from src.contexts.auth.domain.aggregates import User
from src.contexts.auth.domain.errors import UserNotFoundError
from src.contexts.auth.domain.services import ApiKeyHasher
from tests.contexts.auth.conftest import FakeUserRepository


@pytest.mark.unit
class TestCreateApiKeyUseCase:
    async def test_creates_api_key_for_user(
        self, fake_user_repository: FakeUserRepository, sample_user: User
    ) -> None:
        await fake_user_repository.save(sample_user)
        use_case = CreateApiKeyUseCase(fake_user_repository)

        plain_key = await use_case.execute(
            CreateApiKeyDTO(user_id=sample_user.user_id)
        )

        assert isinstance(plain_key, str)
        saved_user = await fake_user_repository.find_by_id(sample_user.user_id)
        assert saved_user is not None
        assert len(saved_user.api_keys) == 1
        assert saved_user.api_keys[0].key_hash == ApiKeyHasher.hash(plain_key)

    async def test_raises_error_for_nonexistent_user(
        self, fake_user_repository: FakeUserRepository
    ) -> None:
        use_case = CreateApiKeyUseCase(fake_user_repository)

        with pytest.raises(UserNotFoundError):
            await use_case.execute(CreateApiKeyDTO(user_id=uuid4()))
