import pytest

from titan.core.investigation import (
    Investigation,
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
