import sqlite3

from titan.application.domain_event_repository import (
    DomainEventRepository,
)
from titan.application.investigation_repository import (
    InvestigationRepository,
)
from titan.application.unit_of_work import UnitOfWork
from titan.infrastructure.sqlite.sqlite_domain_event_repository import (
    SqliteDomainEventRepository,
)
from titan.infrastructure.sqlite.sqlite_investigation_repository import (
    SqliteInvestigationRepository,
)


class SqliteUnitOfWork(UnitOfWork):
    def __init__(
        self,
        database: str,
    ) -> None:
        self._connection = sqlite3.connect(
            database,
        )

        self._investigations = SqliteInvestigationRepository(
            connection=self._connection,
        )
        self._domain_events = SqliteDomainEventRepository(
            connection=self._connection,
        )

        self._connection.commit()

    @property
    def investigations(
        self,
    ) -> InvestigationRepository:
        return self._investigations

    @property
    def domain_events(
        self,
    ) -> DomainEventRepository:
        return self._domain_events

    def commit(
        self,
    ) -> None:
        self._connection.commit()

    def rollback(
        self,
    ) -> None:
        self._connection.rollback()
