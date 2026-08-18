from titan.application.domain_event_repository import (
    DomainEventRepository,
)
from titan.application.investigation_repository import (
    InvestigationRepository,
)
from titan.application.persist_domain_events import (
    persist_domain_events,
)
from titan.core.investigation import Investigation


class CreateInvestigation:
    def __init__(
        self,
        repository: InvestigationRepository,
        event_repository: DomainEventRepository,
    ) -> None:
        self._repository = repository
        self._event_repository = event_repository

    def __call__(
        self,
        title: str,
        purpose: str,
    ) -> Investigation:
        investigation = Investigation.create(
            title=title,
            purpose=purpose,
        )

        self._repository.save(
            investigation,
        )

        persist_domain_events(
            investigation,
            self._event_repository,
        )

        return investigation
