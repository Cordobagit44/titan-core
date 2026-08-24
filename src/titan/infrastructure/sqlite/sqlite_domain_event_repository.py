import sqlite3
from contextlib import nullcontext
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

        self._initialize_schema()

    def _initialize_schema(
        self,
    ) -> None:
        if not self._domain_events_table_exists():
            self._create_domain_events_table(
                "domain_events",
            )

            if self._manages_transaction:
                self._connection.commit()

            return

        if self._domain_events_schema_requires_migration():
            self._migrate_domain_events_schema()

    def _domain_events_table_exists(
        self,
    ) -> bool:
        cursor = self._connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
              AND name = 'domain_events'
            """
        )

        return cursor.fetchone() is not None

    def _domain_events_schema_requires_migration(
        self,
    ) -> bool:
        cursor = self._connection.execute(
            """
            PRAGMA table_info(domain_events)
            """
        )

        columns = {row[1]: row for row in cursor.fetchall()}

        current_columns = {
            "id",
            "event_type",
            "investigation_id",
            "title",
            "closed_at",
            "hypothesis_statement",
            "hypothesis_id",
            "evidence_id",
        }
        columns_missing = bool(current_columns - columns.keys())

        investigation_id_not_nullable = (
            "investigation_id" in columns and columns["investigation_id"][3] == 1
        )

        return columns_missing or investigation_id_not_nullable

    def _create_domain_events_table(
        self,
        table_name: str,
    ) -> None:
        self._connection.execute(
            f"""
            CREATE TABLE {table_name} (
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

    def _migrate_domain_events_schema(
        self,
    ) -> None:
        cursor = self._connection.execute(
            """
            PRAGMA table_info(domain_events)
            """
        )

        existing_columns = {row[1] for row in cursor.fetchall()}

        def optional_column(
            name: str,
        ) -> str:
            return name if name in existing_columns else "NULL"

        investigation_id_expression = optional_column("investigation_id")
        title_expression = optional_column("title")
        closed_at_expression = optional_column("closed_at")
        hypothesis_statement_expression = optional_column("hypothesis_statement")
        hypothesis_id_expression = optional_column("hypothesis_id")
        evidence_id_expression = optional_column("evidence_id")

        transaction = self._connection if self._manages_transaction else nullcontext()

        with transaction:
            self._connection.execute(
                """
                DROP TABLE IF EXISTS domain_events_new
                """
            )

            self._create_domain_events_table(
                "domain_events_new",
            )

            self._connection.execute(
                f"""
                INSERT INTO domain_events_new (
                    id,
                    event_type,
                    investigation_id,
                    title,
                    closed_at,
                    hypothesis_statement,
                    hypothesis_id,
                    evidence_id
                )
                SELECT
                    id,
                    event_type,
                    {investigation_id_expression},
                    {title_expression},
                    {closed_at_expression},
                    {hypothesis_statement_expression},
                    {hypothesis_id_expression},
                    {evidence_id_expression}
                FROM domain_events
                ORDER BY id
                """
            )

            self._connection.execute(
                """
                DROP TABLE domain_events
                """
            )

            self._connection.execute(
                """
                ALTER TABLE domain_events_new
                RENAME TO domain_events
                """
            )

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

        title = (
            event.title
            if isinstance(
                event,
                InvestigationCreated,
            )
            else None
        )

        closed_at = (
            event.closed_at.isoformat()
            if isinstance(
                event,
                InvestigationClosed,
            )
            else None
        )

        hypothesis_statement = (
            event.hypothesis_statement
            if isinstance(
                event,
                HypothesisAdded,
            )
            else None
        )

        hypothesis_id = (
            str(event.hypothesis_id.value)
            if isinstance(
                event,
                HypothesisRemoved | HypothesisConfirmed | HypothesisRejected | EvidenceAdded,
            )
            else None
        )

        evidence_id = (
            str(event.evidence_id.value)
            if isinstance(
                event,
                EvidenceAdded,
            )
            else None
        )

        transaction = self._connection if self._manages_transaction else nullcontext()

        with transaction:
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
