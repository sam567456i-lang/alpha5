from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum
from Backend.core.evidence_dtos.base import BasePlatformObject, BoundaryObject

class StructuralState(Enum):
    """Objective mathematical states. Never subjective interpretations (e.g. Bullish/Bearish)."""
    ASCENDING = "ASCENDING"
    DESCENDING = "DESCENDING"
    EXPANDING = "EXPANDING"
    CONTRACTING = "CONTRACTING"
    NESTED = "NESTED"
    DISCONNECTED = "DISCONNECTED"
    CONTINUOUS = "CONTINUOUS"
    FRAGMENTED = "FRAGMENTED"

@dataclass
class BaseStructureObject(BasePlatformObject):
    """Base primitive for all structure derivations."""
    structural_state: StructuralState = StructuralState.CONTINUOUS

@dataclass
class StructuralBoundaryObject(BoundaryObject):
    """Defines limits of a structural zone without events."""
    structural_state: StructuralState = StructuralState.CONTINUOUS

@dataclass
class InternalStructureObject(StructuralBoundaryObject):
    """Minor/Sub-structural levels mathematically confined within external structures."""
    pass

@dataclass
class ExternalStructureObject(StructuralBoundaryObject):
    """Major/Primary structural levels."""
    pass

@dataclass
class SwingStructureObject(StructuralBoundaryObject):
    """High-timeframe market mapping anchored to major swings."""
    pass

@dataclass
class FractalStructureObject(StructuralBoundaryObject):
    """Self-similar nested boundaries across timeframe limits."""
    pass

@dataclass
class StructuralSegmentObject(BaseStructureObject):
    """Composition of structural legs without boundary limits."""
    pass

@dataclass
class StructuralLegObject(BaseStructureObject):
    """Connects Swing A to Swing B exactly."""
    start_swing_uuid: str = ""
    end_swing_uuid: str = ""
    price_delta: float = 0.0

@dataclass
class StructureHierarchyObject(BaseStructureObject):
    """Maps Parent-Child vertical trees (e.g., Internal bounded by External)."""
    parent_uuid: str = ""
    child_uuids: List[str] = field(default_factory=list)

class TopologyType(Enum):
    ADJACENT = "ADJACENT"
    CONNECTED = "CONNECTED"
    OVERLAPPING = "OVERLAPPING"
    CONTAINS = "CONTAINS"
    INTERSECTS = "INTERSECTS"

@dataclass
class StructureTopologyObject(BaseStructureObject):
    """Maps relational lateral geometry (Adjacent, Connected, Overlapping)."""
    topology_type: TopologyType = TopologyType.ADJACENT
    source_uuid: str = ""
    target_uuid: str = ""
