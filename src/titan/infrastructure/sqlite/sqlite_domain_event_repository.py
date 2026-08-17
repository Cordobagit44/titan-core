import sqlite3
from datetime import datetime
from uuid import UUID

from titan.application.domain_event_repository import (
    DomainEventRepository,
)
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
                investigation_id TEXT NOT NULL,
                title TEXT,
                closed_at TEXT,
                hypothesis_statement TEXT,
                hypothesis_id TEXT
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
            | HypothesisRemoved,
        ):
            raise ValueError(
                "unsupported domain event",
            )

        title = event.title if isinstance(event, InvestigationCreated) else None

        closed_at = event.closed_at.isoformat() if isinstance(event, InvestigationClosed) else None

        hypothesis_statement = (
            event.hypothesis_statement if isinstance(event, HypothesisAdded) else None
        )

        hypothesis_id = (
            str(event.hypothesis_id.value) if isinstance(event, HypothesisRemoved) else None
        )

        with self._connection:
            self._connection.execute(
                """
                INSERT INTO domain_events (
                    event_type,
                    investigation_id,
                    title,
                    closed_at,
                    hypothesis_statement,
                    hypothesis_id
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    type(event).__name__,
                    str(event.investigation_id.value),
                    title,
                    closed_at,
                    hypothesis_statement,
                    hypothesis_id,
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
                hypothesis_id
            FROM domain_events
            ORDER BY id
            """
        )

        events: list[object] = []

        for row in cursor.fetchall():
            investigation_id = InvestigationId(
                value=UUID(row[1]),
            )

            if row[0] == "InvestigationCreated":
                events.append(
                    InvestigationCreated(
                        investigation_id=investigation_id,
                        title=row[2],
                    )
                )
            elif row[0] == "InvestigationActivated":
                events.append(
                    InvestigationActivated(
                        investigation_id=investigation_id,
                    )
                )
            elif row[0] == "InvestigationClosed":
                events.append(
                    InvestigationClosed(
                        investigation_id=investigation_id,
                        closed_at=datetime.fromisoformat(
                            row[3],
                        ),
                    )
                )
            elif row[0] == "InvestigationReopened":
                events.append(
                    InvestigationReopened(
                        investigation_id=investigation_id,
                    )
                )
            elif row[0] == "HypothesisAdded":
                events.append(
                    HypothesisAdded(
                        investigation_id=investigation_id,
                        hypothesis_statement=row[4],
                    )
                )
            elif row[0] == "HypothesisRemoved":
                events.append(
                    HypothesisRemoved(
                        investigation_id=investigation_id,
                        hypothesis_id=HypothesisId(
                            value=UUID(row[5]),
                        ),
                    )
                )

        return events
