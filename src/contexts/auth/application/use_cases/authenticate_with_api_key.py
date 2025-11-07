from src.contexts.auth.domain.errors import InactiveApiKeyError, InvalidApiKeyError
from src.contexts.auth.domain.repositories import UserRepository


class AuthenticateWithApiKeyUseCase:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    async def execute(self, api_key: str) -> bool | None:
        user = await self.user_repository.find_by_api_key(api_key)

        if not user:
            raise InvalidApiKeyError

        api_key_entity = user.find_api_key(api_key)

        if not api_key_entity:
            raise InvalidApiKeyError

        if not api_key_entity.is_active:
            raise InactiveApiKeyError

        return True
