from dataclasses import dataclass, field
from enum import Enum
from uuid import UUID, uuid4

from titan.core.evidence import Evidence


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
class Hypothesis:
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
        if not self.statement.strip():
            raise ValueError("statement must not be empty")

    @property
    def evidences(self) -> tuple[Evidence, ...]:
        return tuple(self._evidences)

    def add_evidence(self, evidence: Evidence) -> None:
        self._evidences.append(evidence)

    def confirm(self) -> None:
        if self.status is HypothesisStatus.REJECTED:
            raise ValueError(
                "rejected hypothesis cannot be confirmed",
            )

        self.status = HypothesisStatus.CONFIRMED

    def reject(self) -> None:
        if self.status is HypothesisStatus.CONFIRMED:
            raise ValueError(
                "confirmed hypothesis cannot be rejected",
            )

        self.status = HypothesisStatus.REJECTED
