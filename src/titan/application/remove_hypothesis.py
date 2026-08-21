from titan.application.persist_domain_events import (
    persist_domain_events,
)
from titan.application.unit_of_work import UnitOfWork
from titan.core.hypothesis import (
    HypothesisId,
)
from titan.core.investigation import (
    InvestigationId,
)


class RemoveHypothesis:
    def __init__(
        self,
        unit_of_work: UnitOfWork,
    ) -> None:
        self._unit_of_work = unit_of_work

    def __call__(
        self,
        investigation_id: InvestigationId,
        hypothesis_id: HypothesisId,
    ) -> None:
        try:
            investigation = self._unit_of_work.investigations.get(
                investigation_id,
            )

            if investigation is None:
                raise LookupError(
                    "investigation not found",
                )

            investigation.remove_hypothesis(
                hypothesis_id,
            )

            self._unit_of_work.investigations.save(
                investigation,
            )

            persist_domain_events(
                investigation,
                self._unit_of_work.domain_events,
            )

            self._unit_of_work.commit()
        except Exception:
            self._unit_of_work.rollback()
            raise
