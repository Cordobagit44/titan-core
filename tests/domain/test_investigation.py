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
