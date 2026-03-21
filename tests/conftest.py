import pytest
from fastapi import FastAPI

from src.main import app as fastapi_app
from tests.support.containers import override_container, user_factory  # noqa: F401
from tests.support.database import (  # noqa: F401
    test_engine,
    test_session_factory,
    test_transaction,
)


@pytest.fixture
def app() -> FastAPI:
    return fastapi_app
