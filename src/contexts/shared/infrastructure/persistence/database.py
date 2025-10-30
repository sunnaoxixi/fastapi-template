from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncEngine

from src.contexts.shared.infrastructure.container import SharedContainer
from src.contexts.shared.infrastructure.persistence.base import Base


async def init_db() -> None:
    container = SharedContainer()
    engine: AsyncEngine = container.engine()

    async with engine.begin() as conn:
        await conn.run_sync(lambda _: None)


async def create_tables() -> None:
    container = SharedContainer()
    engine: AsyncEngine = container.engine()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables() -> None:
    container = SharedContainer()
    engine: AsyncEngine = container.engine()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
