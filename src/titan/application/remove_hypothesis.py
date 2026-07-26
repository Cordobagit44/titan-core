from titan.application.investigation_repository import (
    InvestigationRepository,
)
from titan.core.hypothesis import (
    HypothesisId,
)
from titan.core.investigation import (
    InvestigationId,
)


class RemoveHypothesis:
    def __init__(
        self,
        repository: InvestigationRepository,
    ) -> None:
        self._repository = repository

    def __call__(
        self,
        investigation_id: InvestigationId,
        hypothesis_id: HypothesisId,
    ) -> None:
        investigation = self._repository.get(
            investigation_id,
        )

        if investigation is None:
            raise LookupError(
                "investigation not found",
            )

        investigation.remove_hypothesis(
            hypothesis_id,
        )

        self._repository.save(
            investigation,
        )
