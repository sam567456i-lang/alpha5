from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
from Backend.core.evidence_dtos.base import BasePlatformObject
from Backend.core.evidence_dtos.pattern_components import (
    PatternQuality, Neckline, Peak, Base, Shoulder, Boundary, Apex
)

class PatternLifecycleState(Enum):
    CANDIDATE = "CANDIDATE"
    DEVELOPING = "DEVELOPING"
    CONFIRMED = "CONFIRMED"
    ACTIVE = "ACTIVE"
    BROKEN = "BROKEN"
    INVALIDATED = "INVALIDATED"
    ARCHIVED = "ARCHIVED"

@dataclass
class BasePatternObject(BasePlatformObject):
    """
    Root base for multi-swing Pattern Recognition objects.
    """
    pattern_uuid: str = ""
    lifecycle_state: PatternLifecycleState = PatternLifecycleState.CANDIDATE
    
    # Universal Components
    quality: PatternQuality = field(default_factory=PatternQuality)
    
    # Relationships
    contains_uuids: List[str] = field(default_factory=list)
    overlaps_uuids: List[str] = field(default_factory=list)
    adjacent_uuids: List[str] = field(default_factory=list)
    nested_in_uuid: Optional[str] = None
    continuation_of_uuid: Optional[str] = None
    derived_from_uuid: Optional[str] = None

    # Multi-Timeframe Origin Data
    origin_timeframe: str = ""
    computation_timeframe: str = ""
    publication_timeframe: str = ""

@dataclass
class CompositePatternObject(BasePatternObject):
    """Wrapper holding multiple distinct patterns (e.g., Triangle inside Channel)."""
    member_pattern_uuids: List[str] = field(default_factory=list)

# --- Reversal Patterns ---
@dataclass
class DoubleTop(BasePatternObject):
    peak1: Optional[Peak] = None
    peak2: Optional[Peak] = None
    neckline: Optional[Neckline] = None

@dataclass
class DoubleBottom(BasePatternObject):
    base1: Optional[Base] = None
    base2: Optional[Base] = None
    neckline: Optional[Neckline] = None

@dataclass
class TripleTop(BasePatternObject): pass
@dataclass
class TripleBottom(BasePatternObject): pass

@dataclass
class HeadAndShoulders(BasePatternObject):
    left_shoulder: Optional[Shoulder] = None
    head: Optional[Peak] = None
    right_shoulder: Optional[Shoulder] = None
    neckline: Optional[Neckline] = None

@dataclass
class InverseHeadAndShoulders(BasePatternObject): pass
@dataclass
class RoundedTop(BasePatternObject): pass
@dataclass
class RoundedBottom(BasePatternObject): pass

# --- Continuation Patterns ---
@dataclass
class Flag(BasePatternObject):
    upper_boundary: Optional[Boundary] = None
    lower_boundary: Optional[Boundary] = None
    pole_height: float = 0.0

@dataclass
class Pennant(BasePatternObject): pass
@dataclass
class Rectangle(BasePatternObject): pass
@dataclass
class Channel(BasePatternObject):
    upper_boundary: Optional[Boundary] = None
    lower_boundary: Optional[Boundary] = None

# --- Triangles ---
@dataclass
class AscendingTriangle(BasePatternObject):
    upper_boundary: Optional[Boundary] = None
    lower_boundary: Optional[Boundary] = None
    apex: Optional[Apex] = None

@dataclass
class DescendingTriangle(BasePatternObject): pass
@dataclass
class SymmetricalTriangle(BasePatternObject): pass
@dataclass
class ExpandingTriangle(BasePatternObject): pass

# --- Wedges ---
@dataclass
class RisingWedge(BasePatternObject):
    upper_boundary: Optional[Boundary] = None
    lower_boundary: Optional[Boundary] = None

@dataclass
class FallingWedge(BasePatternObject): pass
@dataclass
class BroadeningWedge(BasePatternObject): pass
