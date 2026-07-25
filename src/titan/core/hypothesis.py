from dataclasses import dataclass, field
from uuid import UUID, uuid4

from titan.core.evidence import Evidence


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
