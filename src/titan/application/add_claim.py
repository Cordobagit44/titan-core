from titan.application.persist_domain_events import persist_domain_events
from titan.application.unit_of_work import UnitOfWork
from titan.core.claim import Claim
from titan.core.evidence import EvidenceId
from titan.core.hypothesis import HypothesisId
from titan.core.investigation import InvestigationId


class AddClaim:
    def __init__(self, unit_of_work: UnitOfWork) -> None:
        self._unit_of_work = unit_of_work

    def __call__(
        self,
        investigation_id: InvestigationId,
        hypothesis_id: HypothesisId,
        evidence_id: EvidenceId,
        statement: str,
    ) -> Claim:
        try:
            investigation = self._unit_of_work.investigations.get(investigation_id)

            if investigation is None:
                raise LookupError("investigation not found")

            claim = Claim(
                statement=statement,
                evidence_id=evidence_id,
            )

            hypothesis = investigation.add_claim(
                hypothesis_id=hypothesis_id,
                claim=claim,
            )

            self._unit_of_work.investigations.save(investigation)
            persist_domain_events(
                hypothesis,
                self._unit_of_work.domain_events,
            )
            self._unit_of_work.commit()

            return claim
        except Exception:
            self._unit_of_work.rollback()
            raise
