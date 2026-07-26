import pytest

from titan.application.activate_investigation import (
    ActivateInvestigation,
)
from titan.application.in_memory_investigation_repository import (
    InMemoryInvestigationRepository,
)
from titan.core.investigation import (
    Investigation,
    InvestigationStatus,
)


def test_activate_investigation_returns_activated_investigation() -> None:
    repository = InMemoryInvestigationRepository()

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )

    repository.save(investigation)

    activate_investigation = ActivateInvestigation(
        repository,
    )

    activated = activate_investigation(
        investigation_id=investigation.id,
    )

    assert activated is investigation
    assert activated.status is InvestigationStatus.ACTIVE


def test_activate_investigation_raises_if_not_found() -> None:
    repository = InMemoryInvestigationRepository()

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )

    activate_investigation = ActivateInvestigation(
        repository,
    )

    with pytest.raises(
        LookupError,
        match="investigation not found",
    ):
        activate_investigation(
            investigation_id=investigation.id,
        )


def test_activate_investigation_preserves_domain_validation() -> None:
    repository = InMemoryInvestigationRepository()

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )

    repository.save(investigation)

    activate_investigation = ActivateInvestigation(
        repository,
    )

    activate_investigation(
        investigation_id=investigation.id,
    )

    with pytest.raises(
        ValueError,
        match="investigation is already active",
    ):
        activate_investigation(
            investigation_id=investigation.id,
        )
