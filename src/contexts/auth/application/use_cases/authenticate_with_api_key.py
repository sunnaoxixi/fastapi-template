from dataclasses import dataclass

from src.contexts.auth.domain.errors import InactiveApiKeyError, InvalidApiKeyError
from src.contexts.auth.domain.repositories import UserRepository
from src.contexts.auth.domain.services import ApiKeyHasher


@dataclass(frozen=True, slots=True)
class AuthenticateWithApiKeyDTO:
    api_key: str


class AuthenticateWithApiKeyUseCase:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    async def execute(self, dto: AuthenticateWithApiKeyDTO) -> None:
        key_hash = ApiKeyHasher.hash(dto.api_key)
        api_key = await self.user_repository.find_api_key_by_hash(key_hash)

        if not api_key:
            raise InvalidApiKeyError

        if not api_key.is_active:
            raise InactiveApiKeyError
