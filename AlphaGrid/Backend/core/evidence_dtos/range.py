from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List, Dict
from datetime import datetime, timedelta
from Backend.core.evidence_dtos.base import BasePlatformObject, BoundaryObject

# --- Phase 2: Core Range Geometry ---

@dataclass
class InternalRangeObject(BoundaryObject):
    """Tracks mathematically objective internal liquidity boundaries."""
    pass

@dataclass
class ExternalRangeObject(BoundaryObject):
    """Tracks mathematically objective external liquidity boundaries."""
    pass

@dataclass
class RangeReferenceObject(BasePlatformObject):
    """Provides metadata describing the original range bounds and duration."""
    start_time: datetime = field(default_factory=datetime.now)
    end_time: datetime = field(default_factory=datetime.now)
    
    @property
    def duration(self) -> timedelta:
        return self.end_time - self.start_time

# --- Geometry Extensions ---

@dataclass
class RangeRatioBoundary(BoundaryObject):
    """
    Exposes generic, objective geometry ratios without methodology-specific interpretation.
    e.g., ratio=0.50 (Equilibrium), 0.75, 0.25.
    """
    ratio: float = 0.50

@dataclass(frozen=True)
class SegmentDefinition:
    name: str
    lower_ratio: float
    upper_ratio: float

@dataclass
class SegmentObject(BoundaryObject):
    """
    Represents an arbitrary configurable segment of the total range.
    """
    definition: Optional[SegmentDefinition] = None

# --- Relationships ---

class RangeRelationshipType(Enum):
    CONTAINS = "CONTAINS"
    OVERLAPS = "OVERLAPS"
    INTERSECTS = "INTERSECTS"
    ADJACENT = "ADJACENT"
    NESTED = "NESTED"
    DISJOINT = "DISJOINT"

@dataclass
class RangeRelationshipObject(BasePlatformObject):
    """
    Purely mathematical facts detailing how two ranges interrelate.
    """
    relationship_type: RangeRelationshipType = RangeRelationshipType.DISJOINT
    source_uuid: str = ""
    target_uuid: str = ""
