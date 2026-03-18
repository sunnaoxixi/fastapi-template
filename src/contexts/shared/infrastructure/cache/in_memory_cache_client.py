import asyncio
from datetime import UTC, datetime, timedelta

from src.contexts.shared.domain.cache_client import CacheClient


class InMemoryCacheClient(CacheClient):
    def __init__(self) -> None:
        self._cache: dict[str, dict[str, object]] = {}
        self._lock = asyncio.Lock()

    async def set(self, key: str, value: object, ttl: int = 600) -> None:
        async with self._lock:
            self._cache[key] = {
                "value": value,
                "expires_at": (
                    datetime.now(tz=UTC) + timedelta(seconds=ttl)
                ).timestamp(),
            }

    async def get(self, key: str) -> object | None:
        async with self._lock:
            item = self._cache.get(key)
            if item:
                if item["expires_at"] > datetime.now(tz=UTC).timestamp():
                    return item["value"]
                self._cache.pop(key, None)
            return None

    async def delete(self, key: str) -> None:
        async with self._lock:
            self._cache.pop(key, None)

    async def clear(self) -> None:
        async with self._lock:
            self._cache.clear()
