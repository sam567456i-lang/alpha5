from dataclasses import dataclass
from typing import List
from Backend.core.analytical_rules.dto.evidence_identity_dto import EvidenceIdentityDTO

from enum import Enum

class RegionType(Enum):
    FVG = "FVG"
    IFVG = "IFVG"
    ORDER_BLOCK = "ORDER_BLOCK"
    BREAKER = "BREAKER"
    MITIGATION_BLOCK = "MITIGATION_BLOCK"
    REJECTION_BLOCK = "REJECTION_BLOCK"
    PROPULSION_BLOCK = "PROPULSION_BLOCK"
    FLIP_ZONE = "FLIP_ZONE"
    LIQUIDITY_VOID = "LIQUIDITY_VOID"
    BPR = "BPR"
    SUPPLY_ZONE = "SUPPLY_ZONE"
    DEMAND_ZONE = "DEMAND_ZONE"
    CUSTOM = "CUSTOM"

@dataclass(frozen=True)
class RegionIdentityDTO:
    """
    Immutable identity for any bounded geometric region.
    This replaces specialized identities like FVGIdentityDTO or PoolIdentityDTO 
    to encourage capability-level reuse across FVGs, Order Blocks, and Voids.
    """
    region_id: str
    region_type: RegionType  # e.g., RegionType.FVG
    anchor_ids: List[str]  # IDs of the evidence that anchors this region (e.g. candle IDs for an FVG)
    graph_namespace: str
    policy_checksum: str
    geometry_fingerprint: str
