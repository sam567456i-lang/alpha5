from dataclasses import dataclass, field
from typing import List

@dataclass(frozen=True)
class DetectorMetadata:
    """
    Standard interface for all detector metadata,
    extracted directly from the Governance Registry.
    """
    ontology_id: str
    capability_id: str
    detector_id: str
    implementation_version: str
    schema_version: str
    lifecycle: str
    
    supported_markets: List[str] = field(default_factory=list)
    supported_timeframes: List[str] = field(default_factory=list)
    supported_sessions: List[str] = field(default_factory=list)
    
    latency_budget_ms: int = 10
    deterministic: bool = True
    replay_supported: bool = True
