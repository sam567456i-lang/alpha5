from dataclasses import dataclass, field
from typing import List, Dict, Any
from Backend.core.analytical_rules.dto.event_evidence_dto import EventEvidenceDTO
from Backend.core.analytical_rules.dto.liquidity.pool_identity import PoolIdentityDTO, PoolSide

@dataclass(frozen=True)
class PoolDetectedEventDTO(EventEvidenceDTO):
    """
    Unified event emitted when a liquidity pool is detected.
    """
    pool_identity: PoolIdentityDTO = None
    
    # Area-based Geometry
    center_price: float = 0.0
    upper_bound: float = 0.0
    lower_bound: float = 0.0
    width: float = 0.0
    anchor_distribution: str = "UNIFORM"
    
    # Provenance and Traceability
    supporting_evidence_ids: List[str] = field(default_factory=list)
    supporting_state_ids: List[str] = field(default_factory=list)
    policy_version: str = "1.0.0"
    detection_reason: str = ""
