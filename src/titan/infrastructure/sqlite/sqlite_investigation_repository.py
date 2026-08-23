import sqlite3
from contextlib import nullcontext
from datetime import datetime
from uuid import UUID

from titan.application.investigation_repository import (
    InvestigationRepository,
)
from titan.core.evidence import (
    Evidence,
    EvidenceId,
    EvidenceRelationship,
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
        database: str | None = None,
        *,
        connection: sqlite3.Connection | None = None,
    ) -> None:
        if connection is not None:
            self._connection = connection
            self._manages_transaction = False
        elif database is not None:
            self._connection = sqlite3.connect(
                database,
            )
            self._manages_transaction = True
        else:
            raise ValueError(
                "database or connection is required",
            )

        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS investigations (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                purpose TEXT NOT NULL,
                status TEXT NOT NULL,
                closed_at TEXT
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

        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS evidences (
                id TEXT PRIMARY KEY,
                hypothesis_id TEXT NOT NULL,
                description TEXT NOT NULL,
                source TEXT NOT NULL,
                relationship TEXT NOT NULL,
                FOREIGN KEY (hypothesis_id)
                    REFERENCES hypotheses (id)
            )
            """
        )

        self._migrate_evidence_schema()

        if self._manages_transaction:
            self._connection.commit()

    def _migrate_evidence_schema(
        self,
    ) -> None:
        columns = {
            row[1]
            for row in self._connection.execute(
                "PRAGMA table_info(evidences)",
            ).fetchall()
        }

        if "source" not in columns:
            self._connection.execute(
                """
                ALTER TABLE evidences
                ADD COLUMN source TEXT NOT NULL
                DEFAULT 'legacy source unavailable'
                """
            )

        if "relationship" not in columns:
            self._connection.execute(
                """
                ALTER TABLE evidences
                ADD COLUMN relationship TEXT NOT NULL
                DEFAULT 'unspecified'
                """
            )

    def save(
        self,
        investigation: Investigation,
    ) -> None:
        investigation_id = str(
            investigation.id.value,
        )

        hypothesis_ids = tuple(str(hypothesis.id.value) for hypothesis in investigation.hypotheses)

        transaction = self._connection if self._manages_transaction else nullcontext()

        with transaction:
            if hypothesis_ids:
                placeholders = ", ".join("?" for _ in hypothesis_ids)

                self._connection.execute(
                    f"""
                    DELETE FROM evidences
                    WHERE hypothesis_id IN ({placeholders})
                    """,
                    hypothesis_ids,
                )

            self._connection.execute(
                """
                DELETE FROM hypotheses
                WHERE investigation_id = ?
                """,
                (investigation_id,),
            )

            self._connection.execute(
                """
                INSERT OR REPLACE INTO investigations (
                    id,
                    title,
                    purpose,
                    status,
                    closed_at
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    investigation_id,
                    investigation.title,
                    investigation.purpose,
                    investigation.status.value,
                    (
                        investigation.closed_at.isoformat()
                        if investigation.closed_at is not None
                        else None
                    ),
                ),
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

            self._connection.executemany(
                """
                INSERT INTO evidences (
                    id,
                    hypothesis_id,
                    description,
                    source,
                    relationship
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    (
                        str(evidence.id.value),
                        str(hypothesis.id.value),
                        evidence.description,
                        evidence.source,
                        evidence.relationship.value,
                    )
                    for hypothesis in investigation.hypotheses
                    for evidence in hypothesis.evidences
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
                status,
                closed_at
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
                status,
                closed_at
            FROM investigations
            ORDER BY rowid
            """
        )

        return tuple(self._to_investigation(row) for row in cursor.fetchall())

    def _to_investigation(
        self,
        row: tuple[str, str, str, str, str | None],
    ) -> Investigation:
        investigation_id = InvestigationId(
            value=UUID(row[0]),
        )

        hypotheses = self._get_hypotheses(
            investigation_id,
        )

        closed_at = datetime.fromisoformat(row[4]) if row[4] is not None else None

        return Investigation.restore(
            investigation_id=investigation_id,
            title=row[1],
            purpose=row[2],
            status=InvestigationStatus(row[3]),
            hypotheses=hypotheses,
            closed_at=closed_at,
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

    def _get_evidences(
        self,
        hypothesis_id: HypothesisId,
    ) -> tuple[Evidence, ...]:
        cursor = self._connection.execute(
            """
            SELECT
                id,
                description,
                source,
                relationship
            FROM evidences
            WHERE hypothesis_id = ?
            ORDER BY rowid
            """,
            (str(hypothesis_id.value),),
        )

        return tuple(
            Evidence(
                id=EvidenceId(
                    value=UUID(row[0]),
                ),
                description=row[1],
                source=row[2],
                relationship=EvidenceRelationship(
                    row[3],
                ),
            )
            for row in cursor.fetchall()
        )

    def _to_hypothesis(
        self,
        row: tuple[str, str, str],
    ) -> Hypothesis:
        hypothesis_id = HypothesisId(
            value=UUID(row[0]),
        )

        hypothesis = Hypothesis(
            id=hypothesis_id,
            statement=row[1],
        )

        for evidence in self._get_evidences(
            hypothesis_id,
        ):
            hypothesis.add_evidence(
                evidence,
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
