from dataclasses import dataclass

from src.contexts.auth.domain.aggregates import User
from src.contexts.auth.domain.repositories import UserRepository
from src.contexts.shared.domain.pagination import CursorParams, CursorResult


@dataclass(frozen=True, slots=True)
class ListUsersDTO:
    cursor: str | None = None
    page_size: int = 20


class ListUsersUseCase:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    async def execute(self, dto: ListUsersDTO) -> CursorResult[User]:
        params = CursorParams(cursor=dto.cursor, page_size=dto.page_size)
        return await self.user_repository.list_paginated(params)
