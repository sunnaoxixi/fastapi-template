from collections.abc import AsyncGenerator

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.main import container
from src.settings import settings


@pytest.fixture(scope="session", autouse=True)
def _wire_container() -> None:
    container.wire()


@pytest.fixture
def test_engine() -> AsyncEngine:
    return create_async_engine(settings.database_url)


@pytest.fixture
async def client(app: FastAPI, test_engine: AsyncEngine) -> AsyncGenerator[AsyncClient]:
    async with test_engine.connect() as conn:
        transaction = await conn.begin()

        test_session_factory = async_sessionmaker(
            bind=conn,
            class_=AsyncSession,
            expire_on_commit=False,
            join_transaction_mode="create_savepoint",
        )

        with (
            container.shared_container.session_factory.override(test_session_factory),
            container.shared_container.engine.override(test_engine),
        ):
            transport = ASGITransport(app=app)
            async with AsyncClient(transport=transport, base_url="http://test") as ac:
                yield ac

        await transaction.rollback()
