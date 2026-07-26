from titan.application.investigation_repository import (
    InvestigationRepository,
)
from titan.core.investigation import (
    Investigation,
    InvestigationId,
)


class GetInvestigation:
    def __init__(
        self,
        repository: InvestigationRepository,
    ) -> None:
        self._repository = repository

    def __call__(
        self,
        investigation_id: InvestigationId,
    ) -> Investigation:
        investigation = self._repository.get(
            investigation_id,
        )

        if investigation is None:
            raise LookupError(
                "investigation not found",
            )

        return investigation
