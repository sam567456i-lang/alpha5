from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass(frozen=True)
class SemanticEvidence:
    """
    Explicitly records the validation logic bridging a ZoneFeature to a Concept.
    Ensures complete explainability for Platform 18 requirements.
    """
    evidence_id: str
    criteria_met: List[str]
    supporting_metrics: Dict[str, Any] = field(default_factory=dict)
    
    # Traceability links
    supporting_zone_id: str = ""
    supporting_structure_ids: List[str] = field(default_factory=list)
    supporting_liquidity_ids: List[str] = field(default_factory=list)
    supporting_volume_nodes: List[str] = field(default_factory=list)
    
    detector_version: str = "1.0.0"
