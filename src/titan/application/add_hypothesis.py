from titan.application.investigation_repository import (
    InvestigationRepository,
)
from titan.core.hypothesis import Hypothesis
from titan.core.investigation import InvestigationId


class AddHypothesis:
    def __init__(
        self,
        repository: InvestigationRepository,
    ) -> None:
        self._repository = repository

    def __call__(
        self,
        investigation_id: InvestigationId,
        statement: str,
    ) -> Hypothesis:
        investigation = self._repository.get(investigation_id)

        if investigation is None:
            raise LookupError("investigation not found")

        investigation.add_hypothesis(statement)

        hypothesis = investigation.hypotheses[-1]

        self._repository.save(investigation)

        return hypothesis
