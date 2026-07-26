from titan.application.investigation_repository import (
    InvestigationRepository,
)
from titan.core.investigation import Investigation


class CreateInvestigation:
    def __init__(
        self,
        repository: InvestigationRepository,
    ) -> None:
        self._repository = repository

    def __call__(
        self,
        title: str,
        purpose: str,
    ) -> Investigation:
        investigation = Investigation.create(
            title=title,
            purpose=purpose,
        )

        self._repository.save(investigation)

        return investigation
