from titan.application.persist_domain_events import persist_domain_events
from titan.application.unit_of_work import UnitOfWork
from titan.core.claim import ClaimId
from titan.core.hypothesis import HypothesisId
from titan.core.interpretation import Interpretation
from titan.core.investigation import InvestigationId


class AddInterpretation:
    def __init__(self, unit_of_work: UnitOfWork) -> None:
        self._unit_of_work = unit_of_work

    def __call__(
        self,
        investigation_id: InvestigationId,
        hypothesis_id: HypothesisId,
        claim_id: ClaimId,
        rationale: str,
    ) -> Interpretation:
        try:
            investigation = self._unit_of_work.investigations.get(investigation_id)

            if investigation is None:
                raise LookupError("investigation not found")

            interpretation = Interpretation(
                claim_id=claim_id,
                hypothesis_id=hypothesis_id,
                rationale=rationale,
            )

            hypothesis = investigation.add_interpretation(
                hypothesis_id=hypothesis_id,
                interpretation=interpretation,
            )

            self._unit_of_work.investigations.save(investigation)
            persist_domain_events(
                hypothesis,
                self._unit_of_work.domain_events,
            )
            self._unit_of_work.commit()

            return interpretation
        except Exception:
            self._unit_of_work.rollback()
            raise
