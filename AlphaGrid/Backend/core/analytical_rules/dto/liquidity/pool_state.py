from dataclasses import dataclass, field
from typing import List, Optional
from Backend.core.analytical_rules.dto.evidence_dto import EvidenceDTO
from Backend.core.analytical_rules.dto.liquidity.pool_identity import PoolIdentityDTO

@dataclass(frozen=True)
class PoolState(EvidenceDTO):
    """
    Mutable projection representing the lifecycle-managed state of a Liquidity Pool.
    Mapped to the `liquidity/default` namespace.
    """
    pool_identity: PoolIdentityDTO = None
    
    # Area-based Geometry
    center_price: float = 0.0
    upper_bound: float = 0.0
    lower_bound: float = 0.0
    width: float = 0.0
    anchor_distribution: str = "UNIFORM"
    
    # Lifecycle Metadata
    created_by_event: str = ""
    created_at: str = ""
    valid_from: str = ""
    last_updated: str = ""
    active: bool = True
    
    # Edges/Relationships (avoiding mutating fields like merged_into)
    parent_pool_id: Optional[str] = None
    derived_pool_ids: List[str] = field(default_factory=list)
    superseded_by: Optional[str] = None
    invalidated_by: Optional[str] = None
    consumed_by: Optional[str] = None
    
    # Provenance
    supporting_evidence_ids: List[str] = field(default_factory=list)
    confidence_inputs: List[str] = field(default_factory=list)
