from titan.application.persist_domain_events import persist_domain_events
from titan.application.unit_of_work import UnitOfWork
from titan.core.assessment import Assessment
from titan.core.investigation import InvestigationId
from titan.core.thesis import ThesisId


class AddAssessment:
    def __init__(self, unit_of_work: UnitOfWork) -> None:
        self._unit_of_work = unit_of_work

    def __call__(
        self,
        investigation_id: InvestigationId,
        thesis_id: ThesisId,
        narrative: str,
    ) -> Assessment:
        try:
            investigation = self._unit_of_work.investigations.get(investigation_id)

            if investigation is None:
                raise LookupError("investigation not found")

            assessment = Assessment(thesis_id=thesis_id, narrative=narrative)
            investigation.add_assessment(assessment)
            self._unit_of_work.investigations.save(investigation)
            persist_domain_events(investigation, self._unit_of_work.domain_events)
            self._unit_of_work.commit()
            return assessment
        except Exception:
            self._unit_of_work.rollback()
            raise
