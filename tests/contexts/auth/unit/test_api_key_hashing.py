import pytest

from src.contexts.auth.domain.services import ApiKeyHasher


@pytest.mark.unit
class TestApiKeyHashing:
    def test_returns_sha256_hex_digest(self) -> None:
        result = ApiKeyHasher.hash("test-key")

        assert (
            result
            == "2e09cae720b4474c3bf1c67e43a1af3bcbb74f654afc0f4cba6de94e2346f564"
        )

    def test_is_deterministic(self) -> None:
        first = ApiKeyHasher.hash("same-key")
        second = ApiKeyHasher.hash("same-key")

        assert first == second

    def test_produces_64_char_hex_string(self) -> None:
        result = ApiKeyHasher.hash("any-key")

        assert len(result) == 64
        assert all(c in "0123456789abcdef" for c in result)
