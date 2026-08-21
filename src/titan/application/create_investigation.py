from titan.application.persist_domain_events import (
    persist_domain_events,
)
from titan.application.unit_of_work import UnitOfWork
from titan.core.investigation import Investigation


class CreateInvestigation:
    def __init__(
        self,
        unit_of_work: UnitOfWork,
    ) -> None:
        self._unit_of_work = unit_of_work

    def __call__(
        self,
        title: str,
        purpose: str,
    ) -> Investigation:
        try:
            investigation = Investigation.create(
                title=title,
                purpose=purpose,
            )

            self._unit_of_work.investigations.save(
                investigation,
            )

            persist_domain_events(
                investigation,
                self._unit_of_work.domain_events,
            )

            self._unit_of_work.commit()

            return investigation
        except Exception:
            self._unit_of_work.rollback()
            raise
