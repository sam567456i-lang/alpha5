from dataclasses import dataclass, field
from typing import List, Dict, Any
from enum import Enum

class CapabilityCertification(Enum):
    IMPLEMENTED = "implemented"
    VERIFIED = "verified"
    REPLAY_TESTED = "replay_tested"
    STREAMING_TESTED = "streaming_tested"
    PERFORMANCE_TESTED = "performance_tested"
    FROZEN = "frozen"

@dataclass
class AnalyticalManifest:
    """Self-documenting contract defining exactly what a capability consumes and produces."""
    capability_id: str
    version: str
    certification_status: CapabilityCertification
    
    inputs: List[str] = field(default_factory=list)
    outputs: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    required_features: List[str] = field(default_factory=list)
    supported_evidence_types: List[str] = field(default_factory=list)
    linked_policies: List[str] = field(default_factory=list)
    tests_passing: bool = False
