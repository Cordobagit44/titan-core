from dataclasses import dataclass, field
from enum import Enum
from uuid import UUID, uuid4

from titan.core.entity import Entity
from titan.core.events import (
    EvidenceAdded,
    HypothesisConfirmed,
    HypothesisRejected,
)
from titan.core.evidence import Evidence

type HypothesisEvent = EvidenceAdded | HypothesisConfirmed | HypothesisRejected


class HypothesisStatus(Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    REJECTED = "REJECTED"


@dataclass(frozen=True)
class HypothesisId:
    value: UUID

    @classmethod
    def new(cls) -> "HypothesisId":
        return cls(value=uuid4())


@dataclass
class Hypothesis(Entity[HypothesisEvent]):
    statement: str
    id: HypothesisId = field(default_factory=HypothesisId.new)
    status: HypothesisStatus = field(
        default=HypothesisStatus.PENDING,
        init=False,
    )
    _evidences: list[Evidence] = field(
        default_factory=list,
        init=False,
        repr=False,
    )

    def __post_init__(self) -> None:
        super().__init__()

        if not self.statement.strip():
            raise ValueError(
                "statement must not be empty",
            )

    @property
    def evidences(self) -> tuple[Evidence, ...]:
        return tuple(self._evidences)

    def add_evidence(
        self,
        evidence: Evidence,
    ) -> None:
        if self.status is not HypothesisStatus.PENDING:
            raise ValueError(
                "decided hypothesis cannot accept evidence",
            )

        self._evidences.append(
            evidence,
        )

        self._record_event(
            EvidenceAdded(
                hypothesis_id=self.id,
                evidence_id=evidence.id,
            )
        )

    def confirm(self) -> None:
        if self.status is HypothesisStatus.CONFIRMED:
            raise ValueError(
                "hypothesis is already confirmed",
            )

        if self.status is HypothesisStatus.REJECTED:
            raise ValueError(
                "rejected hypothesis cannot be confirmed",
            )

        self.status = HypothesisStatus.CONFIRMED
        self._record_event(
            HypothesisConfirmed(
                hypothesis_id=self.id,
            )
        )

    def reject(self) -> None:
        if self.status is HypothesisStatus.REJECTED:
            raise ValueError(
                "hypothesis is already rejected",
            )

        if self.status is HypothesisStatus.CONFIRMED:
            raise ValueError(
                "confirmed hypothesis cannot be rejected",
            )

        self.status = HypothesisStatus.REJECTED
        self._record_event(
            HypothesisRejected(
                hypothesis_id=self.id,
            )
        )
