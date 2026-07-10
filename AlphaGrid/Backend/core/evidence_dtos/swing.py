from dataclasses import dataclass, field
from typing import Optional, List

@dataclass(frozen=True)
class PivotEvidence:
    asset: str
    timeframe: str
    timestamp: int
    pivot_type: str  # "High", "Low"
    price: float

@dataclass(frozen=True)
class PivotLifecycleEvidence:
    asset: str
    timeframe: str
    timestamp: int
    pivot_type: str
    price: float
    state: str  # "Candidate", "Developing", "Confirmed", "Active", "Invalidated", "Archived"

@dataclass(frozen=True)
class SwingClassificationEvidence:
    asset: str
    timeframe: str
    timestamp: int
    classification: str  # "Major", "Intermediate", "Minor"

@dataclass(frozen=True)
class SwingRelationshipEvidence:
    asset: str
    timeframe: str
    timestamp: int
    relationship: str  # "HH", "HL", "LH", "LL", "EQH", "EQL", "NEQH", "NEQL", "HEQ", "LEQ"
    origin_pivot_timestamp: int
    current_pivot_timestamp: int

@dataclass(frozen=True)
class SwingHierarchyEvidence:
    asset: str
    timeframe: str
    timestamp: int
    tree_depth: int
    parent_swing_timestamp: Optional[int]
    child_swings: List[int] = field(default_factory=list)

@dataclass(frozen=True)
class SwingQualityEvidence:
    asset: str
    timeframe: str
    timestamp: int
    magnitude: float
    duration: int
    symmetry_ratio: float
    volatility_adjusted_significance: float
    confirmation_bars: int
    volume_support: float
