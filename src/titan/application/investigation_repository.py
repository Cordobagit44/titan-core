from abc import ABC, abstractmethod

from titan.core.investigation import (
    Investigation,
    InvestigationId,
)


class InvestigationRepository(ABC):
    @abstractmethod
    def get(
        self,
        investigation_id: InvestigationId,
    ) -> Investigation | None:
        raise NotImplementedError

    @abstractmethod
    def save(
        self,
        investigation: Investigation,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def list(self) -> tuple[Investigation, ...]:
        raise NotImplementedError
