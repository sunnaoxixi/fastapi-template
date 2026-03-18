from abc import ABC, abstractmethod


class CacheClient(ABC):
    @abstractmethod
    async def get(self, key: str) -> object | None: ...

    @abstractmethod
    async def set(self, key: str, value: object, ttl: int = 600) -> None: ...

    @abstractmethod
    async def delete(self, key: str) -> None: ...

    @abstractmethod
    async def clear(self) -> None: ...
