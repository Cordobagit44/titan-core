from titan.application.domain_event_repository import (
    DomainEventRepository,
)
from titan.application.investigation_repository import (
    InvestigationRepository,
)
from titan.application.persist_domain_events import (
    persist_domain_events,
)
from titan.core.evidence import Evidence
from titan.core.hypothesis import (
    HypothesisId,
)
from titan.core.investigation import InvestigationId


class AddEvidence:
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
        hypothesis_id: HypothesisId,
        description: str,
    ) -> Evidence:
        investigation = self._repository.get(
            investigation_id,
        )

        if investigation is None:
            raise LookupError(
                "investigation not found",
            )

        hypothesis = investigation.find_hypothesis(
            hypothesis_id,
        )

        if hypothesis is None:
            raise LookupError(
                "hypothesis not found",
            )

        evidence = Evidence(
            description=description,
        )

        hypothesis.add_evidence(
            evidence,
        )

        self._repository.save(
            investigation,
        )

        persist_domain_events(
            hypothesis,
            self._event_repository,
        )

        return evidence
