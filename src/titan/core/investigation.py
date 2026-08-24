from dataclasses import dataclass
from datetime import UTC, datetime
from enum import Enum
from uuid import UUID, uuid4

from titan.core.claim import Claim
from titan.core.entity import Entity
from titan.core.evidence import Evidence
from titan.core.hypothesis import Hypothesis, HypothesisId, HypothesisStatus
from titan.core.interpretation import Interpretation


class InvestigationStatus(Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    CLOSED = "closed"


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
class InvestigationClosed:
    investigation_id: InvestigationId
    closed_at: datetime


@dataclass(frozen=True)
class InvestigationReopened:
    investigation_id: InvestigationId


@dataclass(frozen=True)
class HypothesisAdded:
    investigation_id: InvestigationId
    hypothesis_statement: str


@dataclass(frozen=True)
class HypothesisRemoved:
    investigation_id: InvestigationId
    hypothesis_id: HypothesisId


type DomainEvent = (
    InvestigationCreated
    | InvestigationActivated
    | InvestigationClosed
    | InvestigationReopened
    | HypothesisAdded
    | HypothesisRemoved
)


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
        self.closed_at: datetime | None = None
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

        if not purpose.strip():
            raise ValueError("purpose must not be empty")

        return cls(
            investigation_id=InvestigationId.new(),
            title=title,
            purpose=purpose,
        )

    @classmethod
    def restore(
        cls,
        investigation_id: InvestigationId,
        title: str,
        purpose: str,
        status: InvestigationStatus,
        hypotheses: tuple[Hypothesis, ...],
        closed_at: datetime | None = None,
    ) -> "Investigation":
        normalized_statements = [hypothesis.statement.strip() for hypothesis in hypotheses]

        if len(normalized_statements) != len(set(normalized_statements)):
            raise ValueError("hypothesis already exists")

        evidence_ids = [
            evidence.id for hypothesis in hypotheses for evidence in hypothesis.evidences
        ]

        if len(evidence_ids) != len(set(evidence_ids)):
            raise ValueError("evidence already belongs to another hypothesis")

        investigation = cls(
            investigation_id=investigation_id,
            title=title,
            purpose=purpose,
        )

        investigation.status = status
        investigation.closed_at = closed_at
        investigation._hypotheses.extend(hypotheses)
        investigation.pull_events()

        return investigation

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

    def add_evidence(
        self,
        hypothesis_id: HypothesisId,
        evidence: Evidence,
    ) -> Hypothesis:
        if self.status is InvestigationStatus.CLOSED:
            raise ValueError("investigation is closed")

        hypothesis = self.find_hypothesis(
            hypothesis_id,
        )

        if hypothesis is None:
            raise LookupError(
                "hypothesis not found",
            )

        if any(
            existing.id == evidence.id
            for owner in self._hypotheses
            if owner.id != hypothesis.id
            for existing in owner.evidences
        ):
            raise ValueError(
                "evidence already belongs to another hypothesis",
            )

        hypothesis.add_evidence(
            evidence,
        )

        return hypothesis

    def add_claim(
        self,
        hypothesis_id: HypothesisId,
        claim: Claim,
    ) -> Hypothesis:
        if self.status is InvestigationStatus.CLOSED:
            raise ValueError("investigation is closed")

        hypothesis = self.find_hypothesis(
            hypothesis_id,
        )

        if hypothesis is None:
            raise LookupError(
                "hypothesis not found",
            )

        hypothesis.add_claim(
            claim,
        )

        return hypothesis

    def add_interpretation(
        self,
        hypothesis_id: HypothesisId,
        interpretation: Interpretation,
    ) -> Hypothesis:
        if self.status is InvestigationStatus.CLOSED:
            raise ValueError("investigation is closed")

        hypothesis = self.find_hypothesis(hypothesis_id)

        if hypothesis is None:
            raise LookupError("hypothesis not found")

        hypothesis.add_interpretation(interpretation)

        return hypothesis

    def confirm_hypothesis(
        self,
        hypothesis_id: HypothesisId,
    ) -> Hypothesis:
        if self.status is InvestigationStatus.CLOSED:
            raise ValueError("investigation is closed")

        hypothesis = self.find_hypothesis(
            hypothesis_id,
        )

        if hypothesis is None:
            raise LookupError(
                "hypothesis not found",
            )

        hypothesis.confirm()

        return hypothesis

    def reject_hypothesis(
        self,
        hypothesis_id: HypothesisId,
    ) -> Hypothesis:
        if self.status is InvestigationStatus.CLOSED:
            raise ValueError("investigation is closed")

        hypothesis = self.find_hypothesis(
            hypothesis_id,
        )

        if hypothesis is None:
            raise LookupError(
                "hypothesis not found",
            )

        hypothesis.reject()

        return hypothesis

    def add_hypothesis(
        self,
        statement: str,
    ) -> None:
        if self.status is InvestigationStatus.CLOSED:
            raise ValueError("investigation is closed")

        hypothesis = Hypothesis(statement=statement)

        if any(
            existing.statement.strip() == hypothesis.statement.strip()
            for existing in self._hypotheses
        ):
            raise ValueError("hypothesis already exists")

        self._hypotheses.append(hypothesis)

        self._record_event(
            HypothesisAdded(
                investigation_id=self.id,
                hypothesis_statement=hypothesis.statement,
            )
        )

    def remove_hypothesis(
        self,
        hypothesis_id: HypothesisId,
    ) -> None:
        if self.status is InvestigationStatus.CLOSED:
            raise ValueError("investigation is closed")

        hypothesis = self.find_hypothesis(
            hypothesis_id,
        )

        if hypothesis is None:
            raise LookupError(
                "hypothesis not found",
            )

        if hypothesis.status is not HypothesisStatus.PENDING:
            raise ValueError(
                "decided hypothesis cannot be removed",
            )

        self._hypotheses.remove(
            hypothesis,
        )

        self._record_event(
            HypothesisRemoved(
                investigation_id=self.id,
                hypothesis_id=hypothesis.id,
            )
        )

    def activate(self) -> None:
        if self.status is InvestigationStatus.CLOSED:
            raise ValueError("investigation is closed")

        if self.status is InvestigationStatus.ACTIVE:
            raise ValueError("investigation is already active")

        self.status = InvestigationStatus.ACTIVE

        self._record_event(
            InvestigationActivated(
                investigation_id=self.id,
            )
        )

    def close(self) -> None:
        if self.status is InvestigationStatus.CLOSED:
            raise ValueError("investigation is already closed")

        closed_at = datetime.now(UTC)

        self.status = InvestigationStatus.CLOSED
        self.closed_at = closed_at

        self._record_event(
            InvestigationClosed(
                investigation_id=self.id,
                closed_at=closed_at,
            )
        )

    def reopen(self) -> None:
        if self.status is not InvestigationStatus.CLOSED:
            raise ValueError("investigation is not closed")

        self.status = InvestigationStatus.ACTIVE
        self.closed_at = None

        self._record_event(
            InvestigationReopened(
                investigation_id=self.id,
            )
        )
