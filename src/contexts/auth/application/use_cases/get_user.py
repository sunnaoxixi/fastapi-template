from dataclasses import dataclass
from uuid import UUID

from src.contexts.auth.domain.aggregates import User
from src.contexts.auth.domain.errors import UserNotFoundError
from src.contexts.auth.domain.repositories import UserRepository


@dataclass(frozen=True, slots=True)
class GetUserDTO:
    user_id: UUID


class GetUserUseCase:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    async def execute(self, dto: GetUserDTO) -> User:
        user = await self.user_repository.find_by_id(dto.user_id)
        if not user:
            raise UserNotFoundError(dto.user_id)
        return user
