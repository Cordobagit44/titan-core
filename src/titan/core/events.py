from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from titan.core.claim import ClaimId
    from titan.core.evidence import EvidenceId
    from titan.core.hypothesis import HypothesisId
    from titan.core.interpretation import InterpretationId


@dataclass(frozen=True)
class EvidenceAdded:
    hypothesis_id: "HypothesisId"
    evidence_id: "EvidenceId"


@dataclass(frozen=True)
class ClaimAdded:
    hypothesis_id: "HypothesisId"
    claim_id: "ClaimId"
    evidence_id: "EvidenceId"


@dataclass(frozen=True)
class InterpretationAdded:
    hypothesis_id: "HypothesisId"
    interpretation_id: "InterpretationId"
    claim_id: "ClaimId"


@dataclass(frozen=True)
class HypothesisConfirmed:
    hypothesis_id: "HypothesisId"


@dataclass(frozen=True)
class HypothesisRejected:
    hypothesis_id: "HypothesisId"
