import sqlite3
from pathlib import Path

import pytest

from titan.core.claim import Claim
from titan.core.events import (
    ClaimAdded,
    EvidenceAdded,
    HypothesisConfirmed,
    HypothesisRejected,
    InterpretationAdded,
)
from titan.core.evidence import (
    Evidence,
    EvidenceRelationship,
)
from titan.core.hypothesis import Hypothesis
from titan.core.interpretation import Interpretation
from titan.core.investigation import (
    Investigation,
    InvestigationCreated,
    InvestigationId,
)
from titan.infrastructure.sqlite.sqlite_domain_event_repository import (
    SqliteDomainEventRepository,
)


def test_save_and_list_domain_event() -> None:
    repository = SqliteDomainEventRepository(
        ":memory:",
    )

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )

    event = investigation.pull_events()[0]

    repository.save(
        event,
    )

    events = repository.list_all()

    assert events == [event]


def test_domain_events_survive_repository_reinstantiation(
    tmp_path: Path,
) -> None:
    database = str(
        tmp_path / "domain_events.db",
    )

    repository = SqliteDomainEventRepository(
        database,
    )

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )

    event = investigation.pull_events()[0]

    repository.save(
        event,
    )

    restored_repository = SqliteDomainEventRepository(
        database,
    )

    assert restored_repository.list_all() == [event]


def test_multiple_domain_events_are_preserved_in_order() -> None:
    repository = SqliteDomainEventRepository(
        ":memory:",
    )

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )

    created_event = investigation.pull_events()[0]

    investigation.activate()
    activated_event = investigation.pull_events()[0]

    repository.save(
        created_event,
    )
    repository.save(
        activated_event,
    )

    assert repository.list_all() == [
        created_event,
        activated_event,
    ]


def test_closed_event_preserves_closure_timestamp() -> None:
    repository = SqliteDomainEventRepository(
        ":memory:",
    )

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )

    investigation.pull_events()

    investigation.close()
    closed_event = investigation.pull_events()[0]

    repository.save(
        closed_event,
    )

    assert repository.list_all() == [
        closed_event,
    ]


def test_reopened_event_is_persisted() -> None:
    repository = SqliteDomainEventRepository(
        ":memory:",
    )

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )

    investigation.pull_events()

    investigation.close()
    investigation.pull_events()

    investigation.reopen()
    reopened_event = investigation.pull_events()[0]

    repository.save(
        reopened_event,
    )

    assert repository.list_all() == [
        reopened_event,
    ]


def test_hypothesis_added_event_is_persisted() -> None:
    repository = SqliteDomainEventRepository(
        ":memory:",
    )

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )

    investigation.pull_events()

    investigation.add_hypothesis(
        "Methane indicates microbial life",
    )
    hypothesis_added_event = investigation.pull_events()[0]

    repository.save(
        hypothesis_added_event,
    )

    assert repository.list_all() == [
        hypothesis_added_event,
    ]


def test_hypothesis_removed_event_is_persisted() -> None:
    repository = SqliteDomainEventRepository(
        ":memory:",
    )

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )

    investigation.pull_events()

    investigation.add_hypothesis(
        "Methane indicates microbial life",
    )
    investigation.pull_events()

    hypothesis = investigation.hypotheses[0]

    investigation.remove_hypothesis(
        hypothesis.id,
    )
    hypothesis_removed_event = investigation.pull_events()[0]

    repository.save(
        hypothesis_removed_event,
    )

    assert repository.list_all() == [
        hypothesis_removed_event,
    ]


def test_hypothesis_confirmed_event_is_persisted() -> None:
    repository = SqliteDomainEventRepository(
        ":memory:",
    )

    hypothesis = Hypothesis(
        statement="Methane indicates microbial life",
    )

    hypothesis.confirm()
    confirmed_event = hypothesis.pull_events()[0]

    repository.save(
        confirmed_event,
    )

    assert repository.list_all() == [
        HypothesisConfirmed(
            hypothesis_id=hypothesis.id,
        )
    ]


def test_hypothesis_rejected_event_is_persisted() -> None:
    repository = SqliteDomainEventRepository(
        ":memory:",
    )

    hypothesis = Hypothesis(
        statement="Methane indicates microbial life",
    )

    hypothesis.reject()
    rejected_event = hypothesis.pull_events()[0]

    repository.save(
        rejected_event,
    )

    assert repository.list_all() == [
        HypothesisRejected(
            hypothesis_id=hypothesis.id,
        )
    ]


def test_evidence_added_event_is_persisted() -> None:
    repository = SqliteDomainEventRepository(
        ":memory:",
    )

    hypothesis = Hypothesis(
        statement="Methane indicates microbial life",
    )
    evidence = Evidence(
        description="Methane levels vary seasonally",
        source="Mars methane observations",
        relationship=EvidenceRelationship.SUPPORTS,
    )

    hypothesis.add_evidence(
        evidence,
    )
    evidence_added_event = hypothesis.pull_events()[0]

    repository.save(
        evidence_added_event,
    )

    assert repository.list_all() == [
        EvidenceAdded(
            hypothesis_id=hypothesis.id,
            evidence_id=evidence.id,
        )
    ]


def test_legacy_domain_event_schema_is_migrated(
    tmp_path: Path,
) -> None:
    database = str(
        tmp_path / "legacy_domain_events.db",
    )

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )
    created_event = investigation.pull_events()[0]

    assert isinstance(
        created_event,
        InvestigationCreated,
    )

    connection = sqlite3.connect(
        database,
    )

    connection.execute(
        """
        CREATE TABLE domain_events (
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

    connection.execute(
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
            type(created_event).__name__,
            str(created_event.investigation_id.value),
            created_event.title,
            None,
            None,
            None,
        ),
    )

    connection.commit()
    connection.close()

    repository = SqliteDomainEventRepository(
        database,
    )

    assert repository.list_all() == [
        InvestigationCreated(
            investigation_id=InvestigationId(
                value=created_event.investigation_id.value,
            ),
            title=created_event.title,
        )
    ]

    hypothesis = Hypothesis(
        statement="Methane indicates microbial life",
    )
    evidence = Evidence(
        description="Methane levels vary seasonally",
        source="Mars methane observations",
        relationship=EvidenceRelationship.SUPPORTS,
    )

    hypothesis.add_evidence(
        evidence,
    )
    evidence_added_event = hypothesis.pull_events()[0]

    repository.save(
        evidence_added_event,
    )

    assert repository.list_all() == [
        created_event,
        EvidenceAdded(
            hypothesis_id=hypothesis.id,
            evidence_id=evidence.id,
        ),
    ]


def test_minimal_domain_event_schema_is_migrated() -> None:
    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )
    created_event = investigation.pull_events()[0]
    assert isinstance(created_event, InvestigationCreated)
    connection = sqlite3.connect(":memory:")
    connection.execute(
        """
        CREATE TABLE domain_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT NOT NULL,
            investigation_id TEXT NOT NULL,
            title TEXT
        )
        """
    )
    connection.execute(
        """
        INSERT INTO domain_events (event_type, investigation_id, title)
        VALUES (?, ?, ?)
        """,
        (
            type(created_event).__name__,
            str(created_event.investigation_id.value),
            created_event.title,
        ),
    )

    repository = SqliteDomainEventRepository(
        connection=connection,
    )
    hypothesis = Hypothesis(
        statement="Methane indicates microbial life",
    )
    evidence = Evidence(
        description="Methane levels vary seasonally",
        source="Mars methane observations",
        relationship=EvidenceRelationship.SUPPORTS,
    )
    hypothesis.add_evidence(evidence)
    evidence_added_event = hypothesis.pull_events()[0]
    repository.save(evidence_added_event)

    assert repository.list_all() == [
        created_event,
        EvidenceAdded(
            hypothesis_id=hypothesis.id,
            evidence_id=evidence.id,
        ),
    ]


def test_unknown_persisted_domain_event_is_rejected() -> None:
    connection = sqlite3.connect(":memory:")
    repository = SqliteDomainEventRepository(
        connection=connection,
    )
    connection.execute(
        """
        INSERT INTO domain_events (event_type)
        VALUES (?)
        """,
        ("FutureDomainEvent",),
    )

    with pytest.raises(
        ValueError,
        match="unsupported persisted domain event type: FutureDomainEvent",
    ):
        repository.list_all()


@pytest.mark.parametrize(
    (
        "event_type",
        "investigation_id",
        "title",
        "closed_at",
        "hypothesis_statement",
        "hypothesis_id",
        "evidence_id",
        "missing_field",
    ),
    [
        ("InvestigationCreated", None, "Mars anomaly", None, None, None, None, "investigation_id"),
        (
            "InvestigationClosed",
            str(InvestigationId.new().value),
            None,
            None,
            None,
            None,
            None,
            "closed_at",
        ),
        (
            "HypothesisAdded",
            str(InvestigationId.new().value),
            None,
            None,
            None,
            None,
            None,
            "hypothesis_statement",
        ),
        (
            "EvidenceAdded",
            None,
            None,
            None,
            None,
            str(InvestigationId.new().value),
            None,
            "evidence_id",
        ),
    ],
)
def test_incomplete_persisted_domain_event_is_rejected(
    event_type: str,
    investigation_id: str | None,
    title: str | None,
    closed_at: str | None,
    hypothesis_statement: str | None,
    hypothesis_id: str | None,
    evidence_id: str | None,
    missing_field: str,
) -> None:
    connection = sqlite3.connect(":memory:")
    repository = SqliteDomainEventRepository(
        connection=connection,
    )
    connection.execute(
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
            event_type,
            investigation_id,
            title,
            closed_at,
            hypothesis_statement,
            hypothesis_id,
            evidence_id,
        ),
    )

    with pytest.raises(
        ValueError,
        match=f"incomplete persisted domain event {event_type}: missing {missing_field}",
    ):
        repository.list_all()


@pytest.mark.parametrize(
    (
        "event_type",
        "investigation_id",
        "title",
        "closed_at",
        "hypothesis_id",
        "evidence_id",
        "malformed_field",
    ),
    [
        (
            "InvestigationCreated",
            "not-a-uuid",
            "Mars anomaly",
            None,
            None,
            None,
            "investigation_id",
        ),
        (
            "InvestigationClosed",
            str(InvestigationId.new().value),
            None,
            "not-a-datetime",
            None,
            None,
            "closed_at",
        ),
        ("HypothesisConfirmed", None, None, None, "not-a-uuid", None, "hypothesis_id"),
        (
            "EvidenceAdded",
            None,
            None,
            None,
            str(InvestigationId.new().value),
            "not-a-uuid",
            "evidence_id",
        ),
    ],
)
def test_malformed_persisted_domain_event_payload_is_reported(
    event_type: str,
    investigation_id: str | None,
    title: str | None,
    closed_at: str | None,
    hypothesis_id: str | None,
    evidence_id: str | None,
    malformed_field: str,
) -> None:
    connection = sqlite3.connect(":memory:")
    repository = SqliteDomainEventRepository(
        connection=connection,
    )
    connection.execute(
        """
        INSERT INTO domain_events (
            event_type,
            investigation_id,
            title,
            closed_at,
            hypothesis_id,
            evidence_id
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            event_type,
            investigation_id,
            title,
            closed_at,
            hypothesis_id,
            evidence_id,
        ),
    )

    with pytest.raises(
        ValueError,
        match=f"malformed persisted domain event {event_type}: invalid {malformed_field}",
    ):
        repository.list_all()


def create_claim_added_event() -> ClaimAdded:
    hypothesis = Hypothesis(statement="Methane indicates microbial activity")
    evidence = Evidence(
        description="Methane varies seasonally",
        source="Mars orbiter",
        relationship=EvidenceRelationship.SUPPORTS,
    )
    hypothesis.add_evidence(evidence)
    hypothesis.pull_events()
    claim = Claim(statement="Methane varies seasonally", evidence_id=evidence.id)
    hypothesis.add_claim(claim)
    event = hypothesis.pull_events()[0]
    assert isinstance(event, ClaimAdded)
    return event


def test_save_and_list_claim_added_event() -> None:
    repository = SqliteDomainEventRepository(":memory:")
    event = create_claim_added_event()

    repository.save(event)

    assert repository.list_all() == [event]


def test_incomplete_claim_added_event_is_rejected() -> None:
    connection = sqlite3.connect(":memory:")
    repository = SqliteDomainEventRepository(connection=connection)
    event = create_claim_added_event()
    connection.execute(
        """
        INSERT INTO domain_events (
            event_type, hypothesis_id, evidence_id
        ) VALUES (?, ?, ?)
        """,
        (
            "ClaimAdded",
            str(event.hypothesis_id.value),
            str(event.evidence_id.value),
        ),
    )

    with pytest.raises(
        ValueError,
        match="incomplete persisted domain event ClaimAdded: missing claim_id",
    ):
        repository.list_all()


def test_malformed_claim_added_id_is_reported() -> None:
    connection = sqlite3.connect(":memory:")
    repository = SqliteDomainEventRepository(connection=connection)
    event = create_claim_added_event()
    connection.execute(
        """
        INSERT INTO domain_events (
            event_type, hypothesis_id, evidence_id, claim_id
        ) VALUES (?, ?, ?, ?)
        """,
        (
            "ClaimAdded",
            str(event.hypothesis_id.value),
            str(event.evidence_id.value),
            "not-a-uuid",
        ),
    )

    with pytest.raises(
        ValueError,
        match="malformed persisted domain event ClaimAdded: invalid claim_id",
    ):
        repository.list_all()


def create_interpretation_added_event() -> InterpretationAdded:
    hypothesis = Hypothesis(statement="Methane indicates microbial activity")
    evidence = Evidence(
        description="Methane varies seasonally",
        source="Mars orbiter",
        relationship=EvidenceRelationship.SUPPORTS,
    )
    hypothesis.add_evidence(evidence)
    claim = Claim(statement="Methane varies seasonally", evidence_id=evidence.id)
    hypothesis.add_claim(claim)
    hypothesis.pull_events()
    interpretation = Interpretation(
        hypothesis_id=hypothesis.id,
        claim_id=claim.id,
        rationale="Seasonality is consistent with an active process",
    )
    hypothesis.add_interpretation(interpretation)
    event = hypothesis.pull_events()[0]
    assert isinstance(event, InterpretationAdded)
    return event


def test_save_and_list_interpretation_added_event() -> None:
    repository = SqliteDomainEventRepository(":memory:")
    event = create_interpretation_added_event()

    repository.save(event)

    assert repository.list_all() == [event]


def test_incomplete_interpretation_added_event_is_rejected() -> None:
    connection = sqlite3.connect(":memory:")
    repository = SqliteDomainEventRepository(connection=connection)
    event = create_interpretation_added_event()
    connection.execute(
        """
        INSERT INTO domain_events (
            event_type, hypothesis_id, claim_id
        ) VALUES (?, ?, ?)
        """,
        (
            "InterpretationAdded",
            str(event.hypothesis_id.value),
            str(event.claim_id.value),
        ),
    )

    with pytest.raises(
        ValueError,
        match=("incomplete persisted domain event InterpretationAdded: missing interpretation_id"),
    ):
        repository.list_all()


def test_malformed_interpretation_added_id_is_reported() -> None:
    connection = sqlite3.connect(":memory:")
    repository = SqliteDomainEventRepository(connection=connection)
    event = create_interpretation_added_event()
    connection.execute(
        """
        INSERT INTO domain_events (
            event_type, hypothesis_id, claim_id, interpretation_id
        ) VALUES (?, ?, ?, ?)
        """,
        (
            "InterpretationAdded",
            str(event.hypothesis_id.value),
            str(event.claim_id.value),
            "not-a-uuid",
        ),
    )

    with pytest.raises(
        ValueError,
        match=("malformed persisted domain event InterpretationAdded: invalid interpretation_id"),
    ):
        repository.list_all()
