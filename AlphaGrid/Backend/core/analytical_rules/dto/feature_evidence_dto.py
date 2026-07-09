from dataclasses import dataclass, field
from typing import List, Dict, Any
from Backend.core.analytical_rules.dto.evidence_dto import EvidenceDTO

@dataclass(frozen=True)
class FeatureEvidenceDTO(EvidenceDTO):
    """Objective feature computed from the Feature Subsystem."""
    feature_id: str = ""
    feature_name: str = ""
    feature_version: str = "1.0"
    symbol_id: str = ""
    lookback: int = 0
    policy_hash: str = ""
    normalization_type: str = "NONE"
    source_candles: List[str] = field(default_factory=list)
    feature_value: float = 0.0
    is_stale: bool = False
