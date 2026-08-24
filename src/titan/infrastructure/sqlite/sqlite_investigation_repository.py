import sqlite3
from contextlib import nullcontext
from datetime import datetime
from uuid import UUID

from titan.application.investigation_repository import (
    InvestigationRepository,
)
from titan.core.claim import Claim, ClaimId
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
from titan.core.interpretation import Interpretation, InterpretationId
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

        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS claims (
                id TEXT PRIMARY KEY,
                hypothesis_id TEXT NOT NULL,
                statement TEXT NOT NULL,
                evidence_id TEXT NOT NULL,
                FOREIGN KEY (hypothesis_id)
                    REFERENCES hypotheses (id),
                FOREIGN KEY (evidence_id)
                    REFERENCES evidences (id)
            )
            """
        )

        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS interpretations (
                id TEXT PRIMARY KEY,
                hypothesis_id TEXT NOT NULL,
                claim_id TEXT NOT NULL,
                rationale TEXT NOT NULL,
                FOREIGN KEY (hypothesis_id)
                    REFERENCES hypotheses (id),
                FOREIGN KEY (claim_id)
                    REFERENCES claims (id)
            )
            """
        )

        self._migrate_investigation_schema()
        self._migrate_evidence_schema()

        if self._manages_transaction:
            self._connection.commit()

    def _migrate_investigation_schema(
        self,
    ) -> None:
        columns = {
            row[1]
            for row in self._connection.execute(
                "PRAGMA table_info(investigations)",
            ).fetchall()
        }

        if "closed_at" not in columns:
            self._connection.execute(
                """
                ALTER TABLE investigations
                ADD COLUMN closed_at TEXT
                """
            )

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

        transaction = self._connection if self._manages_transaction else nullcontext()

        with transaction:
            self._connection.execute(
                """
                DELETE FROM interpretations
                WHERE hypothesis_id IN (
                    SELECT id
                    FROM hypotheses
                    WHERE investigation_id = ?
                )
                """,
                (investigation_id,),
            )

            self._connection.execute(
                """
                DELETE FROM claims
                WHERE hypothesis_id IN (
                    SELECT id
                    FROM hypotheses
                    WHERE investigation_id = ?
                )
                """,
                (investigation_id,),
            )

            self._connection.execute(
                """
                DELETE FROM evidences
                WHERE hypothesis_id IN (
                    SELECT id
                    FROM hypotheses
                    WHERE investigation_id = ?
                )
                """,
                (investigation_id,),
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

            self._connection.executemany(
                """
                INSERT INTO claims (
                    id,
                    hypothesis_id,
                    statement,
                    evidence_id
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    (
                        str(claim.id.value),
                        str(hypothesis.id.value),
                        claim.statement,
                        str(claim.evidence_id.value),
                    )
                    for hypothesis in investigation.hypotheses
                    for claim in hypothesis.claims
                ),
            )

            self._connection.executemany(
                """
                INSERT INTO interpretations (
                    id,
                    hypothesis_id,
                    claim_id,
                    rationale
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    (
                        str(interpretation.id.value),
                        str(hypothesis.id.value),
                        str(interpretation.claim_id.value),
                        interpretation.rationale,
                    )
                    for hypothesis in investigation.hypotheses
                    for interpretation in hypothesis.interpretations
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
            value=self._parse_investigation_id(row[0]),
        )

        hypotheses = self._get_hypotheses(
            investigation_id,
        )

        closed_at = self._parse_closed_at(row[0], row[4]) if row[4] is not None else None

        return Investigation.restore(
            investigation_id=investigation_id,
            title=self._validate_required_text("investigation", row[0], "title", row[1]),
            purpose=self._validate_required_text("investigation", row[0], "purpose", row[2]),
            status=self._parse_investigation_status(row[0], row[3]),
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

        return tuple(self._to_evidence(row) for row in cursor.fetchall())

    def _get_claims(
        self,
        hypothesis_id: HypothesisId,
    ) -> tuple[Claim, ...]:
        cursor = self._connection.execute(
            """
            SELECT
                id,
                statement,
                evidence_id
            FROM claims
            WHERE hypothesis_id = ?
            ORDER BY rowid
            """,
            (str(hypothesis_id.value),),
        )

        return tuple(self._to_claim(row) for row in cursor.fetchall())

    def _get_interpretations(
        self,
        hypothesis_id: HypothesisId,
    ) -> tuple[Interpretation, ...]:
        cursor = self._connection.execute(
            """
            SELECT
                id,
                claim_id,
                rationale
            FROM interpretations
            WHERE hypothesis_id = ?
            ORDER BY rowid
            """,
            (str(hypothesis_id.value),),
        )

        return tuple(self._to_interpretation(hypothesis_id, row) for row in cursor.fetchall())

    def _to_interpretation(
        self,
        hypothesis_id: HypothesisId,
        row: tuple[str, str, str],
    ) -> Interpretation:
        return Interpretation(
            id=InterpretationId(
                value=self._parse_interpretation_id(row[0]),
            ),
            hypothesis_id=hypothesis_id,
            claim_id=ClaimId(
                value=self._parse_interpretation_claim_id(row[0], row[1]),
            ),
            rationale=self._validate_required_text(
                "interpretation",
                row[0],
                "rationale",
                row[2],
            ),
        )

    def _to_claim(
        self,
        row: tuple[str, str, str],
    ) -> Claim:
        return Claim(
            id=ClaimId(
                value=self._parse_claim_id(row[0]),
            ),
            statement=self._validate_required_text(
                "claim",
                row[0],
                "statement",
                row[1],
            ),
            evidence_id=EvidenceId(
                value=self._parse_claim_evidence_id(row[0], row[2]),
            ),
        )

    def _to_evidence(
        self,
        row: tuple[str, str, str, str],
    ) -> Evidence:
        return Evidence(
            id=EvidenceId(
                value=self._parse_evidence_id(row[0]),
            ),
            description=self._validate_required_text("evidence", row[0], "description", row[1]),
            source=self._validate_required_text("evidence", row[0], "source", row[2]),
            relationship=self._parse_evidence_relationship(row[0], row[3]),
        )

    def _to_hypothesis(
        self,
        row: tuple[str, str, str],
    ) -> Hypothesis:
        hypothesis_id = HypothesisId(
            value=self._parse_hypothesis_id(row[0]),
        )

        hypothesis = Hypothesis(
            id=hypothesis_id,
            statement=self._validate_required_text("hypothesis", row[0], "statement", row[1]),
        )

        for evidence in self._get_evidences(
            hypothesis_id,
        ):
            hypothesis.add_evidence(
                evidence,
            )

        for claim in self._get_claims(
            hypothesis_id,
        ):
            hypothesis.add_claim(
                claim,
            )

        for interpretation in self._get_interpretations(
            hypothesis_id,
        ):
            hypothesis.add_interpretation(
                interpretation,
            )

        status = self._parse_hypothesis_status(row[0], row[2])

        if status is HypothesisStatus.CONFIRMED:
            hypothesis.confirm()
        elif status is HypothesisStatus.REJECTED:
            hypothesis.reject()

        hypothesis.pull_events()

        return hypothesis

    @staticmethod
    def _parse_investigation_id(
        value: str,
    ) -> UUID:
        try:
            return UUID(value)
        except ValueError as error:
            raise ValueError(
                "malformed persisted investigation record: invalid id",
            ) from error

    @staticmethod
    def _parse_investigation_status(
        investigation_id: str,
        value: str,
    ) -> InvestigationStatus:
        try:
            return InvestigationStatus(value)
        except ValueError as error:
            raise ValueError(
                f"malformed persisted investigation {investigation_id}: invalid status",
            ) from error

    @staticmethod
    def _parse_closed_at(
        investigation_id: str,
        value: str,
    ) -> datetime:
        try:
            return datetime.fromisoformat(value)
        except ValueError as error:
            raise ValueError(
                f"malformed persisted investigation {investigation_id}: invalid closed_at",
            ) from error

    @staticmethod
    def _parse_hypothesis_id(
        value: str,
    ) -> UUID:
        try:
            return UUID(value)
        except ValueError as error:
            raise ValueError(
                "malformed persisted hypothesis record: invalid id",
            ) from error

    @staticmethod
    def _parse_hypothesis_status(
        hypothesis_id: str,
        value: str,
    ) -> HypothesisStatus:
        try:
            return HypothesisStatus(value)
        except ValueError as error:
            raise ValueError(
                f"malformed persisted hypothesis {hypothesis_id}: invalid status",
            ) from error

    @staticmethod
    def _parse_evidence_id(
        value: str,
    ) -> UUID:
        try:
            return UUID(value)
        except ValueError as error:
            raise ValueError(
                "malformed persisted evidence record: invalid id",
            ) from error

    @staticmethod
    def _parse_evidence_relationship(
        evidence_id: str,
        value: str,
    ) -> EvidenceRelationship:
        try:
            return EvidenceRelationship(value)
        except ValueError as error:
            raise ValueError(
                f"malformed persisted evidence {evidence_id}: invalid relationship",
            ) from error

    @staticmethod
    def _parse_claim_id(
        value: str,
    ) -> UUID:
        try:
            return UUID(value)
        except ValueError as error:
            raise ValueError(
                "malformed persisted claim record: invalid id",
            ) from error

    @staticmethod
    def _parse_claim_evidence_id(
        claim_id: str,
        value: str,
    ) -> UUID:
        try:
            return UUID(value)
        except ValueError as error:
            raise ValueError(
                f"malformed persisted claim {claim_id}: invalid evidence_id",
            ) from error

    @staticmethod
    def _parse_interpretation_id(
        value: str,
    ) -> UUID:
        try:
            return UUID(value)
        except ValueError as error:
            raise ValueError(
                "malformed persisted interpretation record: invalid id",
            ) from error

    @staticmethod
    def _parse_interpretation_claim_id(
        interpretation_id: str,
        value: str,
    ) -> UUID:
        try:
            return UUID(value)
        except ValueError as error:
            raise ValueError(
                f"malformed persisted interpretation {interpretation_id}: invalid claim_id",
            ) from error

    @staticmethod
    def _validate_required_text(
        record_type: str,
        record_id: str,
        field: str,
        value: str,
    ) -> str:
        if not value.strip():
            raise ValueError(
                f"malformed persisted {record_type} {record_id}: invalid {field}",
            )

        return value
