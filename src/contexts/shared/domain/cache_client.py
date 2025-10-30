from __future__ import annotations

from abc import ABC, abstractmethod


class CacheClient(ABC):
    @abstractmethod
    def get(self, key: str) -> any | None: ...

    @abstractmethod
    def set(self, key: str, value: any, ttl: int = 3600) -> None: ...

    @abstractmethod
    def delete(self, key: str) -> None: ...

    @abstractmethod
    def clear(self) -> None: ...
