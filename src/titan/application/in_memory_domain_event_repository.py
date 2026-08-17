from titan.application.domain_event_repository import (
    DomainEventRepository,
)


class InMemoryDomainEventRepository(DomainEventRepository):
    def __init__(self) -> None:
        self._events: list[object] = []

    def save(
        self,
        event: object,
    ) -> None:
        self._events.append(
            event,
        )

    def list_all(
        self,
    ) -> list[object]:
        return list(
            self._events,
        )
