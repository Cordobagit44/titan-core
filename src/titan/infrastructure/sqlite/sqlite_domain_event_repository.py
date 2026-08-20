import sqlite3
from datetime import datetime
from uuid import UUID

from titan.application.domain_event_repository import (
    DomainEventRepository,
)
from titan.core.events import (
    EvidenceAdded,
    HypothesisConfirmed,
    HypothesisRejected,
)
from titan.core.evidence import EvidenceId
from titan.core.hypothesis import HypothesisId
from titan.core.investigation import (
    HypothesisAdded,
    HypothesisRemoved,
    InvestigationActivated,
    InvestigationClosed,
    InvestigationCreated,
    InvestigationId,
    InvestigationReopened,
)


class SqliteDomainEventRepository(
    DomainEventRepository,
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
            CREATE TABLE IF NOT EXISTS domain_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL,
                investigation_id TEXT,
                title TEXT,
                closed_at TEXT,
                hypothesis_statement TEXT,
                hypothesis_id TEXT,
                evidence_id TEXT
            )
            """
        )

        self._connection.commit()

    def save(
        self,
        event: object,
    ) -> None:
        if not isinstance(
            event,
            InvestigationCreated
            | InvestigationActivated
            | InvestigationClosed
            | InvestigationReopened
            | HypothesisAdded
            | HypothesisRemoved
            | HypothesisConfirmed
            | HypothesisRejected
            | EvidenceAdded,
        ):
            raise ValueError(
                "unsupported domain event",
            )

        investigation_id = (
            str(event.investigation_id.value)
            if isinstance(
                event,
                InvestigationCreated
                | InvestigationActivated
                | InvestigationClosed
                | InvestigationReopened
                | HypothesisAdded
                | HypothesisRemoved,
            )
            else None
        )

        title = event.title if isinstance(event, InvestigationCreated) else None

        closed_at = event.closed_at.isoformat() if isinstance(event, InvestigationClosed) else None

        hypothesis_statement = (
            event.hypothesis_statement if isinstance(event, HypothesisAdded) else None
        )

        hypothesis_id = (
            str(event.hypothesis_id.value)
            if isinstance(
                event,
                HypothesisRemoved | HypothesisConfirmed | HypothesisRejected | EvidenceAdded,
            )
            else None
        )

        evidence_id = str(event.evidence_id.value) if isinstance(event, EvidenceAdded) else None

        with self._connection:
            self._connection.execute(
                """
                INSERT INTO domain_events (
                    event_type,
                    investigation_id,
                    title,
                    closed_at,
                    hypothesis_statement,
                    hypothesis_id,
                    evidence_id
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    type(event).__name__,
                    investigation_id,
                    title,
                    closed_at,
                    hypothesis_statement,
                    hypothesis_id,
                    evidence_id,
                ),
            )

    def list_all(
        self,
    ) -> list[object]:
        cursor = self._connection.execute(
            """
            SELECT
                event_type,
                investigation_id,
                title,
                closed_at,
                hypothesis_statement,
                hypothesis_id,
                evidence_id
            FROM domain_events
            ORDER BY id
            """
        )

        events: list[object] = []

        for row in cursor.fetchall():
            event_type = row[0]

            if event_type == "InvestigationCreated":
                events.append(
                    InvestigationCreated(
                        investigation_id=InvestigationId(
                            value=UUID(row[1]),
                        ),
                        title=row[2],
                    )
                )
            elif event_type == "InvestigationActivated":
                events.append(
                    InvestigationActivated(
                        investigation_id=InvestigationId(
                            value=UUID(row[1]),
                        ),
                    )
                )
            elif event_type == "InvestigationClosed":
                events.append(
                    InvestigationClosed(
                        investigation_id=InvestigationId(
                            value=UUID(row[1]),
                        ),
                        closed_at=datetime.fromisoformat(
                            row[3],
                        ),
                    )
                )
            elif event_type == "InvestigationReopened":
                events.append(
                    InvestigationReopened(
                        investigation_id=InvestigationId(
                            value=UUID(row[1]),
                        ),
                    )
                )
            elif event_type == "HypothesisAdded":
                events.append(
                    HypothesisAdded(
                        investigation_id=InvestigationId(
                            value=UUID(row[1]),
                        ),
                        hypothesis_statement=row[4],
                    )
                )
            elif event_type == "HypothesisRemoved":
                events.append(
                    HypothesisRemoved(
                        investigation_id=InvestigationId(
                            value=UUID(row[1]),
                        ),
                        hypothesis_id=HypothesisId(
                            value=UUID(row[5]),
                        ),
                    )
                )
            elif event_type == "HypothesisConfirmed":
                events.append(
                    HypothesisConfirmed(
                        hypothesis_id=HypothesisId(
                            value=UUID(row[5]),
                        ),
                    )
                )
            elif event_type == "HypothesisRejected":
                events.append(
                    HypothesisRejected(
                        hypothesis_id=HypothesisId(
                            value=UUID(row[5]),
                        ),
                    )
                )
            elif event_type == "EvidenceAdded":
                events.append(
                    EvidenceAdded(
                        hypothesis_id=HypothesisId(
                            value=UUID(row[5]),
                        ),
                        evidence_id=EvidenceId(
                            value=UUID(row[6]),
                        ),
                    )
                )

        return events
