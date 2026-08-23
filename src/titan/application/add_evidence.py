from titan.application.persist_domain_events import (
    persist_domain_events,
)
from titan.application.unit_of_work import UnitOfWork
from titan.core.evidence import (
    Evidence,
    EvidenceRelationship,
)
from titan.core.hypothesis import (
    HypothesisId,
)
from titan.core.investigation import InvestigationId


class AddEvidence:
    def __init__(
        self,
        unit_of_work: UnitOfWork,
    ) -> None:
        self._unit_of_work = unit_of_work

    def __call__(
        self,
        investigation_id: InvestigationId,
        hypothesis_id: HypothesisId,
        description: str,
        source: str,
        relationship: EvidenceRelationship,
    ) -> Evidence:
        try:
            investigation = self._unit_of_work.investigations.get(
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

            if relationship is EvidenceRelationship.UNSPECIFIED:
                raise ValueError(
                    "relationship must be specified",
                )

            evidence = Evidence(
                description=description,
                source=source,
                relationship=relationship,
            )

            investigation.add_evidence(
                hypothesis_id=hypothesis_id,
                evidence=evidence,
            )

            self._unit_of_work.investigations.save(
                investigation,
            )

            persist_domain_events(
                hypothesis,
                self._unit_of_work.domain_events,
            )

            self._unit_of_work.commit()

            return evidence
        except Exception:
            self._unit_of_work.rollback()
            raise
