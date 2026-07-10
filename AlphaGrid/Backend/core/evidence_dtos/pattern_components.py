from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class PatternQuality:
    """Standardized quality metrics for all multi-swing patterns."""
    symmetry: float = 1.0
    width_bars: int = 0
    height_price: float = 0.0
    duration_seconds: float = 0.0
    slope: float = 0.0
    touch_count: int = 0
    completion_percentage: float = 0.0
    confidence_interval: float = 0.0
    geometric_error: float = 0.0

@dataclass
class PatternGeometryPolicy:
    """Configurable extraction tolerances."""
    max_geometric_variance_pct: float = 0.005 # 0.5% default tolerance
    min_touch_count: int = 2
    require_strict_alternation: bool = True
    max_duration_bars: int = 200

@dataclass
class DoubleTopPolicy(PatternGeometryPolicy):
    """Specific tolerances for Double Top extraction."""
    max_peak_variance_pct: float = 0.002 # Extremely tight 0.2% variance on peaks
    min_neckline_depth_pct: float = 0.02 # Must pull back at least 2%

# --- Geometric Building Blocks ---
@dataclass
class ComponentBase:
    component_uuid: str = ""
    member_swing_uuids: List[str] = field(default_factory=list)

@dataclass
class Neckline(ComponentBase):
    slope: float = 0.0
    y_intercept: float = 0.0

@dataclass
class Peak(ComponentBase):
    price_level: float = 0.0
    timestamp: float = 0.0

@dataclass
class Base(ComponentBase):
    price_level: float = 0.0
    timestamp: float = 0.0

@dataclass
class Shoulder(ComponentBase):
    price_level: float = 0.0
    timestamp: float = 0.0
    is_left: bool = True

@dataclass
class Boundary(ComponentBase):
    slope: float = 0.0
    y_intercept: float = 0.0
    is_upper: bool = True

@dataclass
class Trendline(Boundary):
    pass

@dataclass
class Apex(ComponentBase):
    intersection_price: float = 0.0
    intersection_time: float = 0.0
