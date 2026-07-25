from dataclasses import dataclass
from enum import Enum
from uuid import UUID, uuid4


class InvestigationStatus(Enum):
    DRAFT = "draft"
    ACTIVE = "active"


@dataclass(frozen=True)
class InvestigationId:
    value: UUID

    @classmethod
    def new(cls) -> "InvestigationId":
        return cls(value=uuid4())


@dataclass(frozen=True)
class InvestigationCreated:
    investigation_id: InvestigationId
    title: str


@dataclass(frozen=True)
class InvestigationActivated:
    investigation_id: InvestigationId


class Investigation:
    def __init__(
        self,
        investigation_id: InvestigationId,
        title: str,
        purpose: str,
    ) -> None:
        self.id = investigation_id
        self.title = title
        self.purpose = purpose
        self.status = InvestigationStatus.DRAFT
        self._events: list[InvestigationCreated | InvestigationActivated] = [
            InvestigationCreated(
                investigation_id=self.id,
                title=title,
            )
        ]

    @classmethod
    def create(cls, title: str, purpose: str) -> "Investigation":
        if not title.strip():
            raise ValueError("title must not be empty")

        return cls(
            investigation_id=InvestigationId.new(),
            title=title,
            purpose=purpose,
        )

    def activate(self) -> None:
        if self.status is InvestigationStatus.ACTIVE:
            raise ValueError("investigation is already active")

        self.status = InvestigationStatus.ACTIVE
        self._events.append(
            InvestigationActivated(
                investigation_id=self.id,
            )
        )

    def pull_events(
        self,
    ) -> list[InvestigationCreated | InvestigationActivated]:
        events = self._events
        self._events = []
        return events
