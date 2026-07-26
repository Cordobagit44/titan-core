import sqlite3
from uuid import UUID

from titan.application.investigation_repository import (
    InvestigationRepository,
)
from titan.core.hypothesis import (
    Hypothesis,
    HypothesisId,
    HypothesisStatus,
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

        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS hypotheses (
                id TEXT PRIMARY KEY,
                investigation_id TEXT NOT NULL,
                statement TEXT NOT NULL,
                status TEXT NOT NULL,
                FOREIGN KEY (investigation_id)
                    REFERENCES investigations (id)
            )
            """
        )

        self._connection.commit()

    def save(
        self,
        investigation: Investigation,
    ) -> None:
        investigation_id = str(
            investigation.id.value,
        )

        with self._connection:
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
                    investigation_id,
                    investigation.title,
                    investigation.purpose,
                    investigation.status.value,
                ),
            )

            self._connection.execute(
                """
                DELETE FROM hypotheses
                WHERE investigation_id = ?
                """,
                (investigation_id,),
            )

            self._connection.executemany(
                """
                INSERT INTO hypotheses (
                    id,
                    investigation_id,
                    statement,
                    status
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    (
                        str(hypothesis.id.value),
                        investigation_id,
                        hypothesis.statement,
                        hypothesis.status.value,
                    )
                    for hypothesis in investigation.hypotheses
                ),
            )

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
        investigation_id = InvestigationId(
            value=UUID(row[0]),
        )

        hypotheses = self._get_hypotheses(
            investigation_id,
        )

        return Investigation.restore(
            investigation_id=investigation_id,
            title=row[1],
            purpose=row[2],
            status=InvestigationStatus(row[3]),
            hypotheses=hypotheses,
        )

    def _get_hypotheses(
        self,
        investigation_id: InvestigationId,
    ) -> tuple[Hypothesis, ...]:
        cursor = self._connection.execute(
            """
            SELECT
                id,
                statement,
                status
            FROM hypotheses
            WHERE investigation_id = ?
            ORDER BY rowid
            """,
            (str(investigation_id.value),),
        )

        return tuple(self._to_hypothesis(row) for row in cursor.fetchall())

    def _to_hypothesis(
        self,
        row: tuple[str, str, str],
    ) -> Hypothesis:
        hypothesis = Hypothesis(
            id=HypothesisId(
                value=UUID(row[0]),
            ),
            statement=row[1],
        )

        status = HypothesisStatus(
            row[2],
        )

        if status is HypothesisStatus.CONFIRMED:
            hypothesis.confirm()
        elif status is HypothesisStatus.REJECTED:
            hypothesis.reject()

        hypothesis.pull_events()

        return hypothesis
