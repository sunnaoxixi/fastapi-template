from __future__ import annotations

from typing import Any

from alembic import op
from sqlalchemy import inspect
from sqlalchemy.engine import Connection
from sqlalchemy.schema import Column


def table_exists(table_name: str) -> bool:
    connection: Connection = op.get_bind()
    inspector = inspect(connection)
    return table_name in inspector.get_table_names()


def column_exists(table_name: str, column_name: str) -> bool:
    connection: Connection = op.get_bind()
    inspector = inspect(connection)
    columns = [col["name"] for col in inspector.get_columns(table_name)]
    return column_name in columns


def index_exists(table_name: str, index_name: str) -> bool:
    connection: Connection = op.get_bind()
    inspector = inspect(connection)
    indexes = [idx["name"] for idx in inspector.get_indexes(table_name)]
    return index_name in indexes


def constraint_exists(table_name: str, constraint_name: str) -> bool:
    connection: Connection = op.get_bind()
    inspector = inspect(connection)

    unique_constraints = inspector.get_unique_constraints(table_name)
    if any(uc["name"] == constraint_name for uc in unique_constraints):
        return True

    check_constraints = inspector.get_check_constraints(table_name)
    if any(cc["name"] == constraint_name for cc in check_constraints):
        return True

    foreign_keys = inspector.get_foreign_keys(table_name)
    return any(fk["name"] == constraint_name for fk in foreign_keys)


def safe_create_index(
    table_name: str,
    index_name: str,
    columns: list[str],
    **kwargs: Any,  # noqa: ANN401
) -> None:
    if not index_exists(table_name, index_name):
        op.create_index(index_name, table_name, columns, **kwargs)


def safe_drop_index(table_name: str, index_name: str) -> None:
    if index_exists(table_name, index_name):
        op.drop_index(index_name, table_name=table_name)


def safe_add_column(table_name: str, column: Column) -> None:
    if not column_exists(table_name, column.name):
        op.add_column(table_name, column)


def safe_drop_column(table_name: str, column_name: str) -> None:
    if column_exists(table_name, column_name):
        op.drop_column(table_name, column_name)
