from dataclasses import dataclass, field
from typing import List, Dict, Any
from Backend.core.evidence_dtos.base import BasePlatformObject, PlatformIdentity, LineageRecord

@dataclass(frozen=True)
class PoolMembership:
    """Immutable, revisioned record of pool membership."""
    member_uuid: str
    added_revision: int
    qualification_rule: str
    qualification_inputs: List[str]
    qualification_revision: int

@dataclass
class PoolGeometry:
    """Mathematical scale representation of the pool."""
    centroid: float = 0.0
    bounding_box_upper: float = 0.0
    bounding_box_lower: float = 0.0
    price_span: float = 0.0
    time_span_seconds: float = 0.0
    member_count: int = 0
    density: float = 0.0
    dispersion: float = 0.0
    overlap_percentage: float = 0.0

@dataclass
class LiquidityPoolObject(BasePlatformObject):
    """
    Composition-only Graph Node.
    Never duplicates raw price levels from its members.
    """
    memberships: List[PoolMembership] = field(default_factory=list)
    geometry: PoolGeometry = field(default_factory=PoolGeometry)

@dataclass
class ReferencePool(LiquidityPoolObject):
    pass

@dataclass
class SwingPool(LiquidityPoolObject):
    pass

@dataclass
class EqualLiquidityPool(LiquidityPoolObject):
    pass

@dataclass
class SessionPool(LiquidityPoolObject):
    pass

@dataclass
class RangePool(LiquidityPoolObject):
    pass

@dataclass
class CompositePool(LiquidityPoolObject):
    pass
