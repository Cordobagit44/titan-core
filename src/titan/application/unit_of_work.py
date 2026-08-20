from abc import ABC, abstractmethod

from titan.application.domain_event_repository import (
    DomainEventRepository,
)
from titan.application.investigation_repository import (
    InvestigationRepository,
)


class UnitOfWork(ABC):
    @property
    @abstractmethod
    def investigations(
        self,
    ) -> InvestigationRepository:
        raise NotImplementedError

    @property
    @abstractmethod
    def domain_events(
        self,
    ) -> DomainEventRepository:
        raise NotImplementedError

    @abstractmethod
    def commit(
        self,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def rollback(
        self,
    ) -> None:
        raise NotImplementedError
