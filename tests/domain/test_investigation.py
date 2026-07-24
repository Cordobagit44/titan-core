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
