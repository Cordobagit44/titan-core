from enum import Enum


class InvestigationStatus(Enum):
    DRAFT = "draft"


class InvestigationCreated:
    pass


class Investigation:
    def __init__(self, title: str, purpose: str) -> None:
        self.title = title
        self.purpose = purpose
        self.status = InvestigationStatus.DRAFT
        self._events = [InvestigationCreated()]

    @classmethod
    def create(cls, title: str, purpose: str) -> "Investigation":
        return cls(title=title, purpose=purpose)

    def pull_events(self) -> list[InvestigationCreated]:
        events = self._events
        self._events = []
        return events
