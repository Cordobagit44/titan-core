from titan.application.domain_event_repository import (
    DomainEventRepository,
)
from titan.application.investigation_repository import (
    InvestigationRepository,
)
from titan.application.persist_domain_events import (
    persist_domain_events,
)
from titan.core.hypothesis import Hypothesis
from titan.core.investigation import InvestigationId


class AddHypothesis:
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
        statement: str,
    ) -> Hypothesis:
        investigation = self._repository.get(
            investigation_id,
        )

        if investigation is None:
            raise LookupError(
                "investigation not found",
            )

        investigation.add_hypothesis(
            statement,
        )

        hypothesis = investigation.hypotheses[-1]

        self._repository.save(
            investigation,
        )

        persist_domain_events(
            investigation,
            self._event_repository,
        )

        return hypothesis
