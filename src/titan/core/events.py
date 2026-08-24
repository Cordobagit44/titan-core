from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from titan.core.claim import ClaimId
    from titan.core.evidence import EvidenceId
    from titan.core.hypothesis import HypothesisId


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
class HypothesisConfirmed:
    hypothesis_id: "HypothesisId"


@dataclass(frozen=True)
class HypothesisRejected:
    hypothesis_id: "HypothesisId"
