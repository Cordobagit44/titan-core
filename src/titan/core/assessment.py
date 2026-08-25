from dataclasses import dataclass, field
from uuid import UUID, uuid4

from titan.core.thesis import ThesisId


@dataclass(frozen=True)
class AssessmentId:
    value: UUID

    @classmethod
    def new(cls) -> "AssessmentId":
        return cls(value=uuid4())


@dataclass(frozen=True)
class Assessment:
    thesis_id: ThesisId
    narrative: str
    id: AssessmentId = field(default_factory=AssessmentId.new)

    def __post_init__(self) -> None:
        if not self.narrative.strip():
            raise ValueError("narrative must not be empty")
