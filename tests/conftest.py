from collections.abc import Iterator
import sqlite3
from typing import Any

import pytest


@pytest.fixture(autouse=True)
def close_sqlite_connections(
    monkeypatch: pytest.MonkeyPatch,
) -> Iterator[None]:
    connections: list[sqlite3.Connection] = []
    connect = sqlite3.connect

    def tracked_connect(*args: Any, **kwargs: Any) -> sqlite3.Connection:
        connection = connect(*args, **kwargs)
        connections.append(connection)
        return connection

    monkeypatch.setattr(sqlite3, "connect", tracked_connect)

    yield

    for connection in connections:
        connection.close()
