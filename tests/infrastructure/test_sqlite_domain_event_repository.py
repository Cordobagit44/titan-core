from pathlib import Path

from titan.core.investigation import Investigation
from titan.infrastructure.sqlite.sqlite_domain_event_repository import (
    SqliteDomainEventRepository,
)


def test_save_and_list_domain_event() -> None:
    repository = SqliteDomainEventRepository(
        ":memory:",
    )

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )

    event = investigation.pull_events()[0]

    repository.save(
        event,
    )

    events = repository.list_all()

    assert events == [event]


def test_domain_events_survive_repository_reinstantiation(
    tmp_path: Path,
) -> None:
    database = str(
        tmp_path / "domain_events.db",
    )

    repository = SqliteDomainEventRepository(
        database,
    )

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )

    event = investigation.pull_events()[0]

    repository.save(
        event,
    )

    restored_repository = SqliteDomainEventRepository(
        database,
    )

    assert restored_repository.list_all() == [event]


def test_multiple_domain_events_are_preserved_in_order() -> None:
    repository = SqliteDomainEventRepository(
        ":memory:",
    )

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )

    created_event = investigation.pull_events()[0]

    investigation.activate()
    activated_event = investigation.pull_events()[0]

    repository.save(
        created_event,
    )
    repository.save(
        activated_event,
    )

    assert repository.list_all() == [
        created_event,
        activated_event,
    ]


def test_closed_event_preserves_closure_timestamp() -> None:
    repository = SqliteDomainEventRepository(
        ":memory:",
    )

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )

    investigation.pull_events()

    investigation.close()
    closed_event = investigation.pull_events()[0]

    repository.save(
        closed_event,
    )

    assert repository.list_all() == [
        closed_event,
    ]


def test_reopened_event_is_persisted() -> None:
    repository = SqliteDomainEventRepository(
        ":memory:",
    )

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )

    investigation.pull_events()

    investigation.close()
    investigation.pull_events()

    investigation.reopen()
    reopened_event = investigation.pull_events()[0]

    repository.save(
        reopened_event,
    )

    assert repository.list_all() == [
        reopened_event,
    ]


def test_hypothesis_added_event_is_persisted() -> None:
    repository = SqliteDomainEventRepository(
        ":memory:",
    )

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )

    investigation.pull_events()

    investigation.add_hypothesis(
        "Methane indicates microbial life",
    )
    hypothesis_added_event = investigation.pull_events()[0]

    repository.save(
        hypothesis_added_event,
    )

    assert repository.list_all() == [
        hypothesis_added_event,
    ]


def test_hypothesis_removed_event_is_persisted() -> None:
    repository = SqliteDomainEventRepository(
        ":memory:",
    )

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )

    investigation.pull_events()

    investigation.add_hypothesis(
        "Methane indicates microbial life",
    )
    investigation.pull_events()

    hypothesis = investigation.hypotheses[0]

    investigation.remove_hypothesis(
        hypothesis.id,
    )
    hypothesis_removed_event = investigation.pull_events()[0]

    repository.save(
        hypothesis_removed_event,
    )

    assert repository.list_all() == [
        hypothesis_removed_event,
    ]
