from dataclasses import dataclass, field
from uuid import UUID, uuid4

from titan.core.claim import ClaimId
from titan.core.hypothesis import HypothesisId


@dataclass(frozen=True)
class InterpretationId:
    value: UUID

    @classmethod
    def new(cls) -> "InterpretationId":
        return cls(value=uuid4())


@dataclass(frozen=True)
class Interpretation:
    claim_id: ClaimId
    hypothesis_id: HypothesisId
    rationale: str
    id: InterpretationId = field(default_factory=InterpretationId.new)

    def __post_init__(self) -> None:
        if not self.rationale.strip():
            raise ValueError("rationale must not be empty")
