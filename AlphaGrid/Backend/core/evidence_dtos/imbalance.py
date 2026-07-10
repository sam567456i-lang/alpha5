from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
from Backend.core.evidence_dtos.base import BasePlatformObject
from Backend.core.evidence_dtos.components import FillGeometry

class ImbalanceLifecycleState(Enum):
    CANDIDATE = "CANDIDATE"
    CONFIRMED = "CONFIRMED"
    ACTIVE = "ACTIVE"
    FILLED = "FILLED"
    INVALIDATED = "INVALIDATED"
    ARCHIVED = "ARCHIVED"

class ImbalanceDirection(Enum):
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"
    NEUTRAL = "NEUTRAL"

@dataclass
class BaseImbalanceObject(BasePlatformObject):
    """
    Root base for Imbalance objects.
    """
    imbalance_uuid: str = ""
    lifecycle_state: ImbalanceLifecycleState = ImbalanceLifecycleState.CANDIDATE
    
    # Universal Component Injection
    fill_geometry: FillGeometry = field(default_factory=FillGeometry)
    
    # Decay & Quality metrics
    age_bars: int = 0
    time_alive_seconds: float = 0.0
    freshness: float = 1.0
    volatility_normalized_size: float = 0.0
    impulse_strength: float = 0.0
    gap_integrity: float = 1.0
    structural_alignment: float = 0.0

    # Relationships
    contains_uuids: List[str] = field(default_factory=list)
    inside_uuid: Optional[str] = None
    overlaps_uuids: List[str] = field(default_factory=list)
    touches_uuids: List[str] = field(default_factory=list)
    adjacent_uuids: List[str] = field(default_factory=list)
    merged_into_uuid: Optional[str] = None
    split_from_uuid: Optional[str] = None


@dataclass
class FVG(BaseImbalanceObject):
    """Explicitly owns mathematical coordinates of a single gap."""
    upper_bound: float = 0.0
    lower_bound: float = 0.0
    width: float = 1.0
    height: float = 0.0
    direction: ImbalanceDirection = ImbalanceDirection.NEUTRAL

@dataclass
class IFVG(FVG):
    """Inverse FVG (Inherits coordinates, changes behavioral interpretation in Platform 11)."""
    pass

@dataclass
class BPR(BaseImbalanceObject):
    """Balanced Price Range mathematically defines overlapping gaps."""
    left_gap_uuid: str = ""
    right_gap_uuid: str = ""
    overlap_upper: float = 0.0
    overlap_lower: float = 0.0

class CompositePolicy(Enum):
    STACKED = "STACKED"
    NESTED = "NESTED"
    MERGED = "MERGED"
    SPLIT = "SPLIT"
    CHAIN = "CHAIN"
    CLUSTER = "CLUSTER"
    OVERLAP = "OVERLAP"
    BRIDGE = "BRIDGE"

@dataclass
class CompositeImbalanceObject(BaseImbalanceObject):
    """Generic aggregation object enforcing composition policies."""
    composition_policy: CompositePolicy = CompositePolicy.CLUSTER
    member_uuids: List[str] = field(default_factory=list)
    composite_upper: float = 0.0
    composite_lower: float = 0.0
