from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import uuid
import time

@dataclass
class RuleEvidence:
    """Generic envelope for all rule-generated evidence."""
    rule_id: str
    rule_version: str
    confidence: float # 0.0 to 1.0
    
    # Generic metadata
    latency_ms: float
    quality_score: float
    provenance_hash: str
    
    # Traceability
    supporting_uuid: List[str] = field(default_factory=list)
    contradicting_uuid: List[str] = field(default_factory=list)
    
    # Core Data
    observed_data: Dict[str, Any] = field(default_factory=dict)
    inferred_data: Dict[str, Any] = field(default_factory=dict)
    
    # The rule-specific payload (e.g. sweep_depth, recovery_speed)
    payload: Dict[str, Any] = field(default_factory=dict)
    
    evidence_id: str = field(default_factory=lambda: str(uuid.uuid4()))
