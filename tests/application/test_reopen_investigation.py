import pytest

from titan.application.in_memory_investigation_repository import (
    InMemoryInvestigationRepository,
)
from titan.application.reopen_investigation import (
    ReopenInvestigation,
)
from titan.core.investigation import (
    Investigation,
    InvestigationStatus,
)


def test_reopen_investigation_returns_active_investigation() -> None:
    repository = InMemoryInvestigationRepository()

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )
    investigation.activate()
    investigation.close()

    repository.save(investigation)

    reopen_investigation = ReopenInvestigation(
        repository,
    )

    reopened = reopen_investigation(
        investigation_id=investigation.id,
    )

    assert reopened is investigation
    assert reopened.status is InvestigationStatus.ACTIVE
    assert reopened.closed_at is None


def test_reopen_investigation_raises_if_not_found() -> None:
    repository = InMemoryInvestigationRepository()

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )

    reopen_investigation = ReopenInvestigation(
        repository,
    )

    with pytest.raises(
        LookupError,
        match="investigation not found",
    ):
        reopen_investigation(
            investigation_id=investigation.id,
        )
