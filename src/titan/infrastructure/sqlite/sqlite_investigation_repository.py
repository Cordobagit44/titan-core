import sqlite3
from uuid import UUID

from titan.application.investigation_repository import (
    InvestigationRepository,
)
from titan.core.investigation import (
    Investigation,
    InvestigationId,
    InvestigationStatus,
)


class SqliteInvestigationRepository(
    InvestigationRepository,
):
    def __init__(
        self,
        database: str,
    ) -> None:
        self._connection = sqlite3.connect(
            database,
        )

        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS investigations (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                purpose TEXT NOT NULL,
                status TEXT NOT NULL
            )
            """
        )

        self._connection.commit()

    def save(
        self,
        investigation: Investigation,
    ) -> None:
        self._connection.execute(
            """
            INSERT OR REPLACE INTO investigations (
                id,
                title,
                purpose,
                status
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                str(investigation.id.value),
                investigation.title,
                investigation.purpose,
                investigation.status.value,
            ),
        )

        self._connection.commit()

    def get(
        self,
        investigation_id: InvestigationId,
    ) -> Investigation | None:
        cursor = self._connection.execute(
            """
            SELECT
                id,
                title,
                purpose,
                status
            FROM investigations
            WHERE id = ?
            """,
            (str(investigation_id.value),),
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return self._to_investigation(
            row,
        )

    def list(
        self,
    ) -> tuple[Investigation, ...]:
        cursor = self._connection.execute(
            """
            SELECT
                id,
                title,
                purpose,
                status
            FROM investigations
            ORDER BY rowid
            """
        )

        return tuple(self._to_investigation(row) for row in cursor.fetchall())

    def _to_investigation(
        self,
        row: tuple[str, str, str, str],
    ) -> Investigation:
        investigation = Investigation(
            investigation_id=InvestigationId(
                value=UUID(row[0]),
            ),
            title=row[1],
            purpose=row[2],
        )

        status = InvestigationStatus(
            row[3],
        )

        if status == InvestigationStatus.ACTIVE:
            investigation.activate()

        investigation.pull_events()

        return investigation
