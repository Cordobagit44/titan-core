from dataclasses import dataclass
from enum import Enum
from uuid import UUID, uuid4

from titan.core.entity import Entity
from titan.core.hypothesis import Hypothesis, HypothesisId


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


@dataclass(frozen=True)
class HypothesisAdded:
    investigation_id: InvestigationId
    hypothesis_statement: str


type DomainEvent = InvestigationCreated | InvestigationActivated | HypothesisAdded


class Investigation(Entity[DomainEvent]):
    def __init__(
        self,
        investigation_id: InvestigationId,
        title: str,
        purpose: str,
    ) -> None:
        super().__init__()

        self.id = investigation_id
        self.title = title
        self.purpose = purpose
        self.status = InvestigationStatus.DRAFT
        self._hypotheses: list[Hypothesis] = []

        self._record_event(
            InvestigationCreated(
                investigation_id=self.id,
                title=title,
            )
        )

    @classmethod
    def create(
        cls,
        title: str,
        purpose: str,
    ) -> "Investigation":
        if not title.strip():
            raise ValueError("title must not be empty")

        return cls(
            investigation_id=InvestigationId.new(),
            title=title,
            purpose=purpose,
        )

    @property
    def hypotheses(self) -> tuple[Hypothesis, ...]:
        return tuple(self._hypotheses)

    def find_hypothesis(
        self,
        hypothesis_id: HypothesisId,
    ) -> Hypothesis | None:
        return next(
            (hypothesis for hypothesis in self._hypotheses if hypothesis.id == hypothesis_id),
            None,
        )

    def add_hypothesis(
        self,
        statement: str,
    ) -> None:
        hypothesis = Hypothesis(statement=statement)

        if any(existing.statement == hypothesis.statement for existing in self._hypotheses):
            raise ValueError("hypothesis already exists")

        self._hypotheses.append(hypothesis)

        self._record_event(
            HypothesisAdded(
                investigation_id=self.id,
                hypothesis_statement=hypothesis.statement,
            )
        )

    def activate(self) -> None:
        if self.status is InvestigationStatus.ACTIVE:
            raise ValueError("investigation is already active")

        self.status = InvestigationStatus.ACTIVE

        self._record_event(
            InvestigationActivated(
                investigation_id=self.id,
            )
        )
