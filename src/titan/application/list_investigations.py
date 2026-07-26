from titan.application.investigation_repository import (
    InvestigationRepository,
)
from titan.core.investigation import Investigation


class ListInvestigations:
    def __init__(
        self,
        repository: InvestigationRepository,
    ) -> None:
        self._repository = repository

    def __call__(self) -> tuple[Investigation, ...]:
        return self._repository.list()
