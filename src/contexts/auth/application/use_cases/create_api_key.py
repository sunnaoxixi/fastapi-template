from dataclasses import dataclass
from uuid import UUID

from src.contexts.auth.domain.errors import UserNotFoundError
from src.contexts.auth.domain.repositories import UserRepository


@dataclass(frozen=True, slots=True)
class CreateApiKeyDTO:
    user_id: UUID


class CreateApiKeyUseCase:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    async def execute(self, dto: CreateApiKeyDTO) -> str:
        user = await self.user_repository.find_by_id(dto.user_id)

        if not user:
            raise UserNotFoundError(dto.user_id)

        _api_key, plain_key = user.create_api_key()

        await self.user_repository.save(user)

        return plain_key
