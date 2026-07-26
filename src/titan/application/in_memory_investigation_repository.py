from titan.application.investigation_repository import (
    InvestigationRepository,
)
from titan.core.investigation import (
    Investigation,
    InvestigationId,
)


class InMemoryInvestigationRepository(
    InvestigationRepository,
):
    def __init__(self) -> None:
        self._investigations: dict[
            InvestigationId,
            Investigation,
        ] = {}

    def save(
        self,
        investigation: Investigation,
    ) -> None:
        self._investigations[investigation.id] = investigation

    def get(
        self,
        investigation_id: InvestigationId,
    ) -> Investigation | None:
        return self._investigations.get(investigation_id)
