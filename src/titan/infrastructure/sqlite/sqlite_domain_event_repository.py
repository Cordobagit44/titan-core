import sqlite3
from contextlib import nullcontext
from datetime import datetime
from uuid import UUID

from titan.application.domain_event_repository import (
    DomainEventRepository,
)
from titan.core.claim import ClaimId
from titan.core.events import (
    ClaimAdded,
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
            "claim_id",
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
                evidence_id TEXT,
                claim_id TEXT
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
        claim_id_expression = optional_column("claim_id")

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
                    evidence_id,
                    claim_id
                )
                SELECT
                    id,
                    event_type,
                    {investigation_id_expression},
                    {title_expression},
                    {closed_at_expression},
                    {hypothesis_statement_expression},
                    {hypothesis_id_expression},
                    {evidence_id_expression},
                    {claim_id_expression}
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
            | EvidenceAdded
            | ClaimAdded,
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
                HypothesisRemoved
                | HypothesisConfirmed
                | HypothesisRejected
                | EvidenceAdded
                | ClaimAdded,
            )
            else None
        )

        evidence_id = (
            str(event.evidence_id.value)
            if isinstance(
                event,
                EvidenceAdded | ClaimAdded,
            )
            else None
        )

        claim_id = (
            str(event.claim_id.value)
            if isinstance(
                event,
                ClaimAdded,
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
                    evidence_id,
                    claim_id
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    type(event).__name__,
                    investigation_id,
                    title,
                    closed_at,
                    hypothesis_statement,
                    hypothesis_id,
                    evidence_id,
                    claim_id,
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
                evidence_id,
                claim_id
            FROM domain_events
            ORDER BY id
            """
        )

        events: list[object] = []
        required_fields = {
            "InvestigationCreated": ((1, "investigation_id"), (2, "title")),
            "InvestigationActivated": ((1, "investigation_id"),),
            "InvestigationClosed": ((1, "investigation_id"), (3, "closed_at")),
            "InvestigationReopened": ((1, "investigation_id"),),
            "HypothesisAdded": ((1, "investigation_id"), (4, "hypothesis_statement")),
            "HypothesisRemoved": ((1, "investigation_id"), (5, "hypothesis_id")),
            "HypothesisConfirmed": ((5, "hypothesis_id"),),
            "HypothesisRejected": ((5, "hypothesis_id"),),
            "EvidenceAdded": ((5, "hypothesis_id"), (6, "evidence_id")),
            "ClaimAdded": (
                (5, "hypothesis_id"),
                (7, "claim_id"),
                (6, "evidence_id"),
            ),
        }
        uuid_fields = {
            "InvestigationCreated": ((1, "investigation_id"),),
            "InvestigationActivated": ((1, "investigation_id"),),
            "InvestigationClosed": ((1, "investigation_id"),),
            "InvestigationReopened": ((1, "investigation_id"),),
            "HypothesisAdded": ((1, "investigation_id"),),
            "HypothesisRemoved": ((1, "investigation_id"), (5, "hypothesis_id")),
            "HypothesisConfirmed": ((5, "hypothesis_id"),),
            "HypothesisRejected": ((5, "hypothesis_id"),),
            "EvidenceAdded": ((5, "hypothesis_id"), (6, "evidence_id")),
            "ClaimAdded": (
                (5, "hypothesis_id"),
                (7, "claim_id"),
                (6, "evidence_id"),
            ),
        }
        datetime_fields = {
            "InvestigationClosed": ((3, "closed_at"),),
        }

        for row in cursor.fetchall():
            event_type = row[0]

            for index, field in required_fields.get(event_type, ()):
                if row[index] is None:
                    raise ValueError(
                        f"incomplete persisted domain event {event_type}: missing {field}",
                    )

            parsed_uuids = {
                index: self._parse_uuid(event_type, field, row[index])
                for index, field in uuid_fields.get(event_type, ())
            }
            parsed_datetimes = {
                index: self._parse_datetime(event_type, field, row[index])
                for index, field in datetime_fields.get(event_type, ())
            }

            if event_type == "InvestigationCreated":
                events.append(
                    InvestigationCreated(
                        investigation_id=InvestigationId(
                            value=parsed_uuids[1],
                        ),
                        title=row[2],
                    )
                )
            elif event_type == "InvestigationActivated":
                events.append(
                    InvestigationActivated(
                        investigation_id=InvestigationId(
                            value=parsed_uuids[1],
                        ),
                    )
                )
            elif event_type == "InvestigationClosed":
                events.append(
                    InvestigationClosed(
                        investigation_id=InvestigationId(
                            value=parsed_uuids[1],
                        ),
                        closed_at=parsed_datetimes[3],
                    )
                )
            elif event_type == "InvestigationReopened":
                events.append(
                    InvestigationReopened(
                        investigation_id=InvestigationId(
                            value=parsed_uuids[1],
                        ),
                    )
                )
            elif event_type == "HypothesisAdded":
                events.append(
                    HypothesisAdded(
                        investigation_id=InvestigationId(
                            value=parsed_uuids[1],
                        ),
                        hypothesis_statement=row[4],
                    )
                )
            elif event_type == "HypothesisRemoved":
                events.append(
                    HypothesisRemoved(
                        investigation_id=InvestigationId(
                            value=parsed_uuids[1],
                        ),
                        hypothesis_id=HypothesisId(
                            value=parsed_uuids[5],
                        ),
                    )
                )
            elif event_type == "HypothesisConfirmed":
                events.append(
                    HypothesisConfirmed(
                        hypothesis_id=HypothesisId(
                            value=parsed_uuids[5],
                        ),
                    )
                )
            elif event_type == "HypothesisRejected":
                events.append(
                    HypothesisRejected(
                        hypothesis_id=HypothesisId(
                            value=parsed_uuids[5],
                        ),
                    )
                )
            elif event_type == "EvidenceAdded":
                events.append(
                    EvidenceAdded(
                        hypothesis_id=HypothesisId(
                            value=parsed_uuids[5],
                        ),
                        evidence_id=EvidenceId(
                            value=parsed_uuids[6],
                        ),
                    )
                )
            elif event_type == "ClaimAdded":
                events.append(
                    ClaimAdded(
                        hypothesis_id=HypothesisId(
                            value=parsed_uuids[5],
                        ),
                        claim_id=ClaimId(
                            value=parsed_uuids[7],
                        ),
                        evidence_id=EvidenceId(
                            value=parsed_uuids[6],
                        ),
                    )
                )
            else:
                raise ValueError(
                    f"unsupported persisted domain event type: {event_type}",
                )

        return events

    @staticmethod
    def _parse_uuid(
        event_type: str,
        field: str,
        value: str,
    ) -> UUID:
        try:
            return UUID(value)
        except ValueError as error:
            raise ValueError(
                f"malformed persisted domain event {event_type}: invalid {field}",
            ) from error

    @staticmethod
    def _parse_datetime(
        event_type: str,
        field: str,
        value: str,
    ) -> datetime:
        try:
            return datetime.fromisoformat(value)
        except ValueError as error:
            raise ValueError(
                f"malformed persisted domain event {event_type}: invalid {field}",
            ) from error
