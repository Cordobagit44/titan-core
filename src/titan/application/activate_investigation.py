from titan.application.domain_event_repository import (
    DomainEventRepository,
)
from titan.application.investigation_repository import (
    InvestigationRepository,
)
from titan.core.investigation import (
    Investigation,
    InvestigationId,
)


class ActivateInvestigation:
    def __init__(
        self,
        repository: InvestigationRepository,
        event_repository: DomainEventRepository,
    ) -> None:
        self._repository = repository
        self._event_repository = event_repository

    def __call__(
        self,
        investigation_id: InvestigationId,
    ) -> Investigation:
        investigation = self._repository.get(
            investigation_id,
        )

        if investigation is None:
            raise LookupError(
                "investigation not found",
            )

        investigation.activate()

        self._repository.save(
            investigation,
        )

        for event in investigation.pull_events():
            self._event_repository.save(
                event,
            )

        return investigation
