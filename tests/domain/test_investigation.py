from datetime import UTC, datetime

import pytest

from titan.core.hypothesis import Hypothesis
from titan.core.investigation import (
    HypothesisAdded,
    Investigation,
    InvestigationActivated,
    InvestigationClosed,
    InvestigationCreated,
    InvestigationId,
    InvestigationStatus,
)


def test_create_investigation_starts_as_draft() -> None:
    investigation = Investigation.create(
        title="NVIDIA Long-Term",
        purpose="Evaluate NVIDIA as a long-term investment.",
    )

    assert investigation.status is InvestigationStatus.DRAFT

    events = investigation.pull_events()

    assert len(events) == 1
    assert isinstance(events[0], InvestigationCreated)


@pytest.mark.parametrize("invalid_title", ["", "   "])
def test_create_investigation_rejects_empty_title(invalid_title: str) -> None:
    with pytest.raises(ValueError, match="title must not be empty"):
        Investigation.create(
            title=invalid_title,
            purpose="Evaluate NVIDIA as a long-term investment.",
        )


@pytest.mark.parametrize("invalid_purpose", ["", "   "])
def test_create_investigation_rejects_empty_purpose(invalid_purpose: str) -> None:
    with pytest.raises(ValueError, match="purpose must not be empty"):
        Investigation.create(
            title="NVIDIA Long-Term",
            purpose=invalid_purpose,
        )


def test_investigation_created_event_contains_title() -> None:
    investigation = Investigation.create(
        title="NVIDIA Long-Term",
        purpose="Investment thesis",
    )

    event = investigation.pull_events()[0]

    assert isinstance(event, InvestigationCreated)
    assert event.title == "NVIDIA Long-Term"


def test_new_investigations_have_different_ids() -> None:
    first = Investigation.create(
        title="NVIDIA Long-Term",
        purpose="Investment thesis",
    )

    second = Investigation.create(
        title="Apple Long-Term",
        purpose="Investment thesis",
    )

    assert first.id != second.id


def test_investigation_created_event_contains_investigation_id() -> None:
    investigation = Investigation.create(
        title="NVIDIA Long-Term",
        purpose="Investment thesis",
    )

    event = investigation.pull_events()[0]

    assert event.investigation_id == investigation.id


def test_activate_investigation_changes_status_to_active() -> None:
    investigation = Investigation.create(
        title="Acme Corp",
        purpose="Evaluate acquisition",
    )

    investigation.activate()

    assert investigation.status is InvestigationStatus.ACTIVE


def test_cannot_activate_an_active_investigation() -> None:
    investigation = Investigation.create(
        title="Acme Corp",
        purpose="Evaluate acquisition",
    )

    investigation.activate()

    with pytest.raises(ValueError, match="investigation is already active"):
        investigation.activate()


def test_activate_investigation_emits_domain_event() -> None:
    investigation = Investigation.create(
        title="Acme Corp",
        purpose="Evaluate acquisition",
    )

    investigation.pull_events()  # descartamos el evento de creación

    investigation.activate()

    events = investigation.pull_events()

    assert len(events) == 1
    assert isinstance(events[0], InvestigationActivated)


def test_add_hypothesis_to_investigation() -> None:
    investigation = Investigation.create(
        title="NVIDIA Long-Term",
        purpose="Investment thesis",
    )

    investigation.add_hypothesis(
        statement="NVIDIA will maintain 20% annual revenue growth.",
    )

    assert len(investigation.hypotheses) == 1
    assert (
        investigation.hypotheses[0].statement == "NVIDIA will maintain 20% annual revenue growth."
    )


def test_add_hypothesis_emits_hypothesis_added_event() -> None:
    investigation = Investigation.create(
        title="Network Intrusion",
        purpose="Determine attack vector",
    )

    investigation.pull_events()

    investigation.add_hypothesis("Credentials were compromised")

    events = investigation.pull_events()

    assert len(events) == 1

    event = events[0]

    assert isinstance(event, HypothesisAdded)
    assert event.investigation_id == investigation.id
    assert event.hypothesis_statement == "Credentials were compromised"


def test_add_hypothesis_rejects_duplicate_statement() -> None:
    investigation = Investigation.create(
        title="Network Intrusion",
        purpose="Determine attack vector",
    )
    investigation.pull_events()

    investigation.add_hypothesis("Credentials were compromised")
    investigation.pull_events()

    with pytest.raises(
        ValueError,
        match="hypothesis already exists",
    ):
        investigation.add_hypothesis("Credentials were compromised")

    assert len(investigation.hypotheses) == 1
    assert investigation.pull_events() == []


def test_add_hypothesis_rejects_whitespace_equivalent_statement() -> None:
    investigation = Investigation.create(
        title="Network Intrusion",
        purpose="Determine attack vector",
    )
    investigation.pull_events()
    investigation.add_hypothesis("Credentials were compromised")
    investigation.pull_events()

    with pytest.raises(
        ValueError,
        match="hypothesis already exists",
    ):
        investigation.add_hypothesis("  Credentials were compromised  ")

    assert len(investigation.hypotheses) == 1
    assert investigation.pull_events() == []


def test_add_hypothesis_duplicate_comparison_remains_case_sensitive() -> None:
    investigation = Investigation.create(
        title="Network Intrusion",
        purpose="Determine attack vector",
    )

    investigation.add_hypothesis("Credentials were compromised")
    investigation.add_hypothesis("credentials were compromised")

    assert len(investigation.hypotheses) == 2


def test_find_hypothesis_returns_matching_hypothesis() -> None:
    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )

    investigation.add_hypothesis(
        "Methane indicates microbial life",
    )

    hypothesis = investigation.hypotheses[0]

    found = investigation.find_hypothesis(
        hypothesis.id,
    )

    assert found is hypothesis


def test_find_hypothesis_returns_none_when_not_found() -> None:
    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )

    unknown_hypothesis = Hypothesis(
        statement="Unknown hypothesis",
    )

    found = investigation.find_hypothesis(
        unknown_hypothesis.id,
    )

    assert found is None


def test_close_investigation_changes_status_to_closed() -> None:
    investigation = Investigation.create(
        title="Acme Corp",
        purpose="Evaluate acquisition",
    )

    investigation.close()

    assert investigation.status is InvestigationStatus.CLOSED


def test_cannot_close_an_already_closed_investigation() -> None:
    investigation = Investigation.create(
        title="Acme Corp",
        purpose="Evaluate acquisition",
    )

    investigation.close()

    with pytest.raises(
        ValueError,
        match="investigation is already closed",
    ):
        investigation.close()


def test_can_close_an_active_investigation() -> None:
    investigation = Investigation.create(
        title="Acme Corp",
        purpose="Evaluate acquisition",
    )

    investigation.activate()
    investigation.close()

    assert investigation.status is InvestigationStatus.CLOSED


def test_cannot_add_hypothesis_to_closed_investigation() -> None:
    investigation = Investigation.create(
        title="Acme Corp",
        purpose="Evaluate acquisition",
    )

    investigation.close()

    with pytest.raises(
        ValueError,
        match="investigation is closed",
    ):
        investigation.add_hypothesis(
            "Revenue will grow 20% annually",
        )


def test_cannot_remove_hypothesis_from_closed_investigation() -> None:
    investigation = Investigation.create(
        title="Acme Corp",
        purpose="Evaluate acquisition",
    )

    investigation.add_hypothesis(
        "Revenue will grow 20% annually",
    )
    hypothesis = investigation.hypotheses[0]

    investigation.close()

    with pytest.raises(
        ValueError,
        match="investigation is closed",
    ):
        investigation.remove_hypothesis(
            hypothesis.id,
        )


def test_cannot_activate_closed_investigation() -> None:
    investigation = Investigation.create(
        title="Acme Corp",
        purpose="Evaluate acquisition",
    )

    investigation.close()

    with pytest.raises(
        ValueError,
        match="investigation is closed",
    ):
        investigation.activate()


def test_reopen_closed_investigation_changes_status_to_active() -> None:
    investigation = Investigation.create(
        title="Acme Corp",
        purpose="Evaluate acquisition",
    )

    investigation.close()
    investigation.reopen()

    assert investigation.status is InvestigationStatus.ACTIVE


def test_cannot_reopen_investigation_that_is_not_closed() -> None:
    investigation = Investigation.create(
        title="Acme Corp",
        purpose="Evaluate acquisition",
    )

    with pytest.raises(
        ValueError,
        match="investigation is not closed",
    ):
        investigation.reopen()


def test_reopened_investigation_allows_hypothesis_modifications() -> None:
    investigation = Investigation.create(
        title="Acme Corp",
        purpose="Evaluate acquisition",
    )

    investigation.close()
    investigation.reopen()

    investigation.add_hypothesis(
        "Revenue will grow 20% annually",
    )
    hypothesis = investigation.hypotheses[0]

    investigation.remove_hypothesis(
        hypothesis.id,
    )

    assert investigation.hypotheses == ()


def test_close_investigation_records_closure_timestamp() -> None:
    investigation = Investigation.create(
        title="Acme Corp",
        purpose="Evaluate acquisition",
    )

    assert investigation.closed_at is None

    investigation.close()

    assert investigation.closed_at is not None
    assert isinstance(investigation.closed_at, datetime)
    assert investigation.closed_at.tzinfo is UTC


def test_reopen_investigation_clears_closure_timestamp() -> None:
    investigation = Investigation.create(
        title="Acme Corp",
        purpose="Evaluate acquisition",
    )

    investigation.close()

    assert investigation.closed_at is not None

    investigation.reopen()

    assert investigation.closed_at is None


def test_close_investigation_emits_closure_event() -> None:
    investigation = Investigation.create(
        title="Acme Corp",
        purpose="Evaluate acquisition",
    )
    investigation.pull_events()

    investigation.close()

    events = investigation.pull_events()

    assert len(events) == 1

    event = events[0]

    assert isinstance(event, InvestigationClosed)
    assert event.investigation_id == investigation.id
    assert event.closed_at == investigation.closed_at


def test_restore_closed_investigation_preserves_closure_timestamp() -> None:
    closed_at = datetime.now(UTC)

    investigation = Investigation.restore(
        investigation_id=InvestigationId.new(),
        title="Acme Corp",
        purpose="Evaluate acquisition",
        status=InvestigationStatus.CLOSED,
        hypotheses=(),
        closed_at=closed_at,
    )

    assert investigation.status is InvestigationStatus.CLOSED
    assert investigation.closed_at == closed_at


@pytest.mark.parametrize(
    "duplicate_statement",
    ["Artificial structure", "  Artificial structure  "],
)
def test_restore_rejects_whitespace_equivalent_hypotheses(
    duplicate_statement: str,
) -> None:
    hypotheses = (
        Hypothesis(statement="Artificial structure"),
        Hypothesis(statement=duplicate_statement),
    )

    with pytest.raises(ValueError, match="hypothesis already exists"):
        Investigation.restore(
            investigation_id=InvestigationId.new(),
            title="Mars anomaly",
            purpose="Find evidence",
            status=InvestigationStatus.DRAFT,
            hypotheses=hypotheses,
        )


def test_restore_accepts_case_distinct_hypotheses() -> None:
    hypotheses = (
        Hypothesis(statement="Artificial structure"),
        Hypothesis(statement="artificial structure"),
    )

    investigation = Investigation.restore(
        investigation_id=InvestigationId.new(),
        title="Mars anomaly",
        purpose="Find evidence",
        status=InvestigationStatus.DRAFT,
        hypotheses=hypotheses,
    )

    assert investigation.hypotheses == hypotheses
    assert investigation.pull_events() == []
