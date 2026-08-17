from inspect import isabstract

from titan.application.domain_event_repository import (
    DomainEventRepository,
)


def test_domain_event_repository_is_abstract() -> None:
    assert isabstract(DomainEventRepository)
