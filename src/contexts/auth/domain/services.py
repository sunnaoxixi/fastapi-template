import hashlib


class ApiKeyHasher:
    @staticmethod
    def hash(key: str) -> str:
        return hashlib.sha256(key.encode()).hexdigest()
