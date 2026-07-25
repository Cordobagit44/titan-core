import pytest

from titan.core.investigation import (
    HypothesisAdded,
    Investigation,
    InvestigationActivated,
    InvestigationCreated,
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
