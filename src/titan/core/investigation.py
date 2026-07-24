from dataclasses import dataclass
from enum import Enum


class InvestigationStatus(Enum):
    DRAFT = "draft"


@dataclass(frozen=True)
class InvestigationCreated:
    title: str


class Investigation:
    def __init__(self, title: str, purpose: str) -> None:
        self.title = title
        self.purpose = purpose
        self.status = InvestigationStatus.DRAFT
        self._events = [InvestigationCreated(title=title)]

    @classmethod
    def create(cls, title: str, purpose: str) -> "Investigation":
        if not title.strip():
            raise ValueError("title must not be empty")

        return cls(title=title, purpose=purpose)

    def pull_events(self) -> list[InvestigationCreated]:
        events = self._events
        self._events = []
        return events
