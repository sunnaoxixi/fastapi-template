from uuid import uuid4

import pytest

from src.contexts.auth.domain.aggregates import User
from src.contexts.auth.domain.errors import ApiKeyNotFoundError
from src.contexts.auth.domain.services import ApiKeyHasher


@pytest.mark.unit
class TestUserAggregate:
    def test_create(self) -> None:
        user = User.create(username="johndoe", password="pass123")

        assert user.username == "johndoe"
        assert user.is_active is True
        assert user.api_keys == []

    def test_create_api_key(self) -> None:
        user = User.create(username="johndoe", password="pass123")

        api_key, plain_key = user.create_api_key()

        assert len(user.api_keys) == 1
        assert api_key.user_id == user.user_id
        assert api_key.is_active is True
        assert api_key.key_hash == ApiKeyHasher.hash(plain_key)

    def test_revoke_api_key(self) -> None:
        user = User.create(username="johndoe", password="pass123")
        api_key, _plain_key = user.create_api_key()

        user.revoke_api_key(api_key.api_key_id)

        assert user.api_keys[0].is_active is False

    def test_revoke_api_key_raises_when_not_found(self) -> None:
        user = User.create(username="johndoe", password="pass123")

        with pytest.raises(ApiKeyNotFoundError):
            user.revoke_api_key(uuid4())

    def test_find_api_key_by_hash(self) -> None:
        user = User.create(username="johndoe", password="pass123")
        api_key, plain_key = user.create_api_key()

        found = user.find_api_key_by_hash(ApiKeyHasher.hash(plain_key))

        assert found is not None
        assert found.api_key_id == api_key.api_key_id
