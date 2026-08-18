from titan.application.domain_event_repository import (
    DomainEventRepository,
)
from titan.core.entity import Entity


def persist_domain_events[EventT](
    entity: Entity[EventT],
    event_repository: DomainEventRepository,
) -> None:
    for event in entity.pull_events():
        event_repository.save(
            event,
        )
