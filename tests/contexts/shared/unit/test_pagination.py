import base64
from datetime import UTC, datetime
from uuid import UUID, uuid4

import pytest

from src.contexts.shared.domain.errors import InvalidCursorError
from src.contexts.shared.domain.pagination import (
    CursorParams,
    decode_cursor,
    encode_cursor,
)


@pytest.mark.unit
class TestCursorParams:
    def test_defaults(self) -> None:
        params = CursorParams()

        assert params.cursor is None
        assert params.page_size == 20

    def test_page_size_zero_raises(self) -> None:
        with pytest.raises(ValueError):
            CursorParams(page_size=0)

    def test_page_size_above_max_raises(self) -> None:
        with pytest.raises(ValueError):
            CursorParams(page_size=101)

    def test_page_size_one_is_valid(self) -> None:
        params = CursorParams(page_size=1)

        assert params.page_size == 1

    def test_page_size_one_hundred_is_valid(self) -> None:
        params = CursorParams(page_size=100)

        assert params.page_size == 100


@pytest.mark.unit
class TestCursorEncoding:
    def test_encode_decode_next_roundtrip(self) -> None:
        entity_id = uuid4()
        created_at = datetime(2024, 6, 15, 12, 30, 0, tzinfo=UTC)

        cursor = encode_cursor("next", created_at, entity_id)
        direction, decoded_at, decoded_id = decode_cursor(cursor)

        assert direction == "next"
        assert decoded_at == created_at
        assert decoded_id == entity_id

    def test_encode_decode_previous_roundtrip(self) -> None:
        entity_id = uuid4()
        created_at = datetime(2025, 1, 1, 0, 0, 0, tzinfo=UTC)

        cursor = encode_cursor("previous", created_at, entity_id)
        direction, decoded_at, decoded_id = decode_cursor(cursor)

        assert direction == "previous"
        assert decoded_at == created_at
        assert decoded_id == entity_id

    def test_decode_malformed_base64_raises(self) -> None:
        with pytest.raises(InvalidCursorError):
            decode_cursor("not-valid-base64!!!")

    def test_decode_valid_base64_invalid_content_raises(self) -> None:
        garbage = base64.b64encode(b"garbage").decode()

        with pytest.raises(InvalidCursorError):
            decode_cursor(garbage)

    def test_decode_wrong_direction_raises(self) -> None:
        entity_id = uuid4()
        created_at = datetime(2024, 1, 1, tzinfo=UTC)
        raw = f"sideways|{created_at.isoformat()}|{entity_id}"
        cursor = base64.b64encode(raw.encode()).decode()

        with pytest.raises(InvalidCursorError):
            decode_cursor(cursor)

    def test_decode_naive_datetime_gets_utc(self) -> None:
        entity_id = uuid4()
        naive_dt = datetime(2024, 3, 10, 8, 0, 0)
        raw = f"next|{naive_dt.isoformat()}|{entity_id}"
        cursor = base64.b64encode(raw.encode()).decode()

        direction, decoded_at, decoded_id = decode_cursor(cursor)

        assert decoded_at.tzinfo is not None
        assert decoded_at == datetime(2024, 3, 10, 8, 0, 0, tzinfo=UTC)
