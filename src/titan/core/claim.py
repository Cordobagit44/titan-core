from dataclasses import dataclass, field
from uuid import UUID, uuid4

from titan.core.evidence import EvidenceId


@dataclass(frozen=True)
class ClaimId:
    value: UUID

    @classmethod
    def new(cls) -> "ClaimId":
        return cls(value=uuid4())


@dataclass(frozen=True)
class Claim:
    statement: str
    evidence_id: EvidenceId
    id: ClaimId = field(default_factory=ClaimId.new)

    def __post_init__(self) -> None:
        if not self.statement.strip():
            raise ValueError("statement must not be empty")
