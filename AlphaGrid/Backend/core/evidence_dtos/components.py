from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class FillGeometry:
    """
    Universal reusable component for measuring partial/full geometric fills.
    Will be aggregated into FVGs, Order Blocks, Liquidity Pools, etc.
    """
    filled_height: float = 0.0
    remaining_height: float = 0.0
    fill_percent: float = 0.0
    deepest_penetration: float = 0.0
    first_touch: Optional[datetime] = None
    last_touch: Optional[datetime] = None
    fill_velocity: float = 0.0
    time_to_fill_seconds: float = 0.0
