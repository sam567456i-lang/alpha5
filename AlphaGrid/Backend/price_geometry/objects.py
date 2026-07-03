from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
import hashlib
import json

class LifecycleState(Enum):
    DETECTED = "DETECTED"
    CONFIRMED = "CONFIRMED"
    BROKEN = "BROKEN"
    RETESTED = "RETESTED"
    INVALIDATED = "INVALIDATED"
    ARCHIVED = "ARCHIVED"

@dataclass(frozen=True)
class GeometryObject:
    """Base immutable geometry object."""
    id: str
    version: str
    dataset_id: str
    symbol: str
    timeframe: str
    timestamp: datetime
    price: float
    generator: str = ""
    source_bars: List[str] = field(default_factory=list)
    parent_ids: List[str] = field(default_factory=list)
    child_ids: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 1.0
    quality: float = 1.0
    lifecycle_state: LifecycleState = LifecycleState.DETECTED

    @property
    def fingerprint(self) -> str:
        """Deterministic hash of the geometry object's state."""
        state = {
            "id": self.id,
            "version": self.version,
            "dataset_id": self.dataset_id,
            "symbol": self.symbol,
            "timeframe": self.timeframe,
            "timestamp": self.timestamp.isoformat(),
            "price": self.price,
            "source_bars": sorted(self.source_bars),
            "parent_ids": sorted(self.parent_ids),
            "lifecycle_state": self.lifecycle_state.value
        }
        encoded = json.dumps(state, sort_keys=True).encode('utf-8')
        return hashlib.sha256(encoded).hexdigest()

    def evolve(self, **kwargs) -> 'GeometryObject':
        """
        Creates a new immutable instance with updated fields and bumped version.
        Useful for tracing state transitions without mutating objects in place.
        """
        import dataclasses
        
        # Simple version bumping: v1.0.0 -> v1.0.0-1 -> v1.0.0-2
        current_v = self.version
        if '-' in current_v:
            base, rev = current_v.rsplit('-', 1)
            if rev.isdigit():
                new_v = f"{base}-{int(rev)+1}"
            else:
                new_v = f"{current_v}-1"
        else:
            new_v = f"{current_v}-1"
            
        kwargs.setdefault('version', new_v)
        return dataclasses.replace(self, **kwargs)

@dataclass(frozen=True)
class Pivot(GeometryObject):
    is_high: bool = True
    left_bars: int = 3
    right_bars: int = 3

@dataclass(frozen=True)
class Trendline(GeometryObject):
    start_point_id: str = ""
    end_point_id: str = ""
    slope: float = 0.0
    is_support: bool = True
    touches: int = 2

@dataclass(frozen=True)
class Channel(GeometryObject):
    upper_trendline_id: str = ""
    lower_trendline_id: str = ""
    is_ascending: bool = True
    width: float = 0.0

@dataclass(frozen=True)
class Range(GeometryObject):
    top_price: float = 0.0
    bottom_price: float = 0.0
    start_timestamp: datetime = field(default_factory=datetime.utcnow)
    end_timestamp: Optional[datetime] = None
    is_broken: bool = False

@dataclass(frozen=True)
class Swing(GeometryObject):
    is_high: bool = True
    strength: int = 3
    is_internal: bool = True

@dataclass(frozen=True)
class Structure(GeometryObject):
    structure_type: str = "BOS"  # BOS, CHOCH, MSS
    is_bullish: bool = True
    is_internal: bool = True

@dataclass(frozen=True)
class Liquidity(GeometryObject):
    pool_type: str = "EQH"  # EQH, EQL, BSL, SSL, INTERNAL, EXTERNAL
    decay_policy: str = "MITIGATION"
    
@dataclass(frozen=True)
class Imbalance(GeometryObject):
    imbalance_type: str = "FVG"
    is_bullish: bool = True
    top_price: float = 0.0
    bottom_price: float = 0.0
    mitigated_price: Optional[float] = None
    size: float = 0.0
    filled_pct: float = 0.0

@dataclass(frozen=True)
class Zone(GeometryObject):
    zone_type: str = "PREMIUM" # PREMIUM, DISCOUNT, EQUILIBRIUM, SUPPLY, DEMAND, SUPPORT, RESISTANCE
    top_price: float = 0.0
    bottom_price: float = 0.0

@dataclass(frozen=True)
class OrderBlock(GeometryObject):
    ob_type: str = "OB"
    is_bullish: bool = True
    top_price: float = 0.0
    bottom_price: float = 0.0
    mitigated_price: Optional[float] = None
