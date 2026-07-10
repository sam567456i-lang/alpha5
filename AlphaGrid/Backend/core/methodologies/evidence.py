from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum
from datetime import datetime

class ClaimCategory(Enum):
    DIRECTIONAL = "DIRECTIONAL"
    STRUCTURAL = "STRUCTURAL"
    EXECUTION = "EXECUTION"
    RISK = "RISK"
    RESEARCH = "RESEARCH"

@dataclass(frozen=True)
class ExplanationObject:
    """Machine-readable explanation for a claim."""
    explanation_type: str
    reference_id: str
    severity: str
    supporting_uuids: List[str]
    weight: float

@dataclass(frozen=True)
class ConfidenceVector:
    """Multidimensional confidence representation."""
    confidence: float
    data_quality: float
    coverage: float
    agreement: float
    freshness: float
    reliability: float

@dataclass
class MethodologyState:
    """The runtime capability state of a methodology instance."""
    is_enabled: bool = True
    degradation_reason: str = ""

@dataclass
class MethodologyEvidence:
    """Intermediate synthesis before Claim generation."""
    raw_synthesis: Dict[str, Any]

@dataclass(frozen=True)
class MethodologyClaim:
    """The ultimate first-class output published to Platform 12."""
    claim_id: str
    claim_type: str
    category: ClaimCategory
    confidence_vector: ConfidenceVector
    valid_until_bar: int
    invalidation_conditions: List[str]
    evidence_trace: List[str] # Platform 10 UUIDs
    explanation_objects: List[ExplanationObject]
    methodology_version: str
    context_id: str
