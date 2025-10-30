from __future__ import annotations

from datetime import UTC, datetime, timedelta

from src.contexts.shared.domain.cache_client import CacheClient


class InMemoryCacheClient(CacheClient):
    def __init__(self) -> None:
        self._cache = {}

    def set(self, key: str, value: any, ttl: int = 600) -> None:
        self._cache[key] = {
            "value": value,
            "expires_at": datetime.now(tz=UTC).timestamp() + timedelta(seconds=ttl),
        }

    def get(self, key: str) -> any | None:
        item = self._cache.get(key)
        if item:
            if item["expires_at"] > datetime.now(tz=UTC).timestamp():
                return item["value"]
            self.delete(key)
        return None

    def delete(self, key: str) -> None:
        self._cache.pop(key, None)

    def clear(self) -> None:
        self._cache.clear()
