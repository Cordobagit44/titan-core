import pytest

from titan.application.close_investigation import (
    CloseInvestigation,
)
from titan.application.in_memory_investigation_repository import (
    InMemoryInvestigationRepository,
)
from titan.core.investigation import (
    Investigation,
    InvestigationStatus,
)


def test_close_investigation_returns_closed_investigation() -> None:
    repository = InMemoryInvestigationRepository()

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )
    investigation.activate()

    repository.save(investigation)

    close_investigation = CloseInvestigation(
        repository,
    )

    closed = close_investigation(
        investigation_id=investigation.id,
    )

    assert closed is investigation
    assert closed.status is InvestigationStatus.CLOSED


def test_close_investigation_raises_if_not_found() -> None:
    repository = InMemoryInvestigationRepository()

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )

    close_investigation = CloseInvestigation(
        repository,
    )

    with pytest.raises(
        LookupError,
        match="investigation not found",
    ):
        close_investigation(
            investigation_id=investigation.id,
        )
