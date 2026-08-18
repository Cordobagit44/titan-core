from titan.application.domain_event_repository import (
    DomainEventRepository,
)
from titan.application.investigation_repository import (
    InvestigationRepository,
)
from titan.application.persist_domain_events import (
    persist_domain_events,
)
from titan.core.investigation import (
    Investigation,
    InvestigationId,
)


class ReopenInvestigation:
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

        investigation.reopen()

        self._repository.save(
            investigation,
        )

        persist_domain_events(
            investigation,
            self._event_repository,
        )

        return investigation
