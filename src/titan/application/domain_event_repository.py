from abc import ABC, abstractmethod


class DomainEventRepository(ABC):
    @abstractmethod
    def save(
        self,
        event: object,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def list_all(
        self,
    ) -> list[object]:
        raise NotImplementedError
