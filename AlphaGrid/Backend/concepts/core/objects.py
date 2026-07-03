from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, Optional
import hashlib
import json
from Backend.price_geometry.objects import LifecycleState

@dataclass(frozen=True)
class ConceptObject:
    """Base immutable concept object."""
    id: str
    version: str
    dataset_id: str
    timeframe: str
    timestamp: datetime
    concept_type: str  # e.g., ORDER_BLOCK, PIN_BAR, LIQUIDITY_SWEEP
    is_bullish: bool
    price: float
    # Provenance linking to GeometryGraph nodes
    geometry_dependency_ids: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    lifecycle_state: LifecycleState = LifecycleState.DETECTED
    
    @property
    def fingerprint(self) -> str:
        """Deterministic hash of the concept object's state."""
        state = {
            "id": self.id,
            "version": self.version,
            "dataset_id": self.dataset_id,
            "timeframe": self.timeframe,
            "timestamp": self.timestamp.isoformat(),
            "concept_type": self.concept_type,
            "is_bullish": self.is_bullish,
            "price": self.price,
            "geometry_dependencies": sorted(self.geometry_dependency_ids),
            "lifecycle_state": self.lifecycle_state.value
        }
        encoded = json.dumps(state, sort_keys=True).encode('utf-8')
        return hashlib.sha256(encoded).hexdigest()

@dataclass(frozen=True)
class CandlestickPattern(ConceptObject):
    """Price Action Concept (e.g., Pin Bar, Engulfing)."""
    pattern_name: str = "UNKNOWN"
    pattern_size_pct: float = 0.0

@dataclass(frozen=True)
class OrderBlock(ConceptObject):
    """SMC Order Block Concept."""
    top_price: float = 0.0
    bottom_price: float = 0.0
    mitigated_price: Optional[float] = None
    
@dataclass(frozen=True)
class BreakerBlock(OrderBlock):
    """SMC Breaker Block."""
    pass
    
@dataclass(frozen=True)
class MitigationBlock(OrderBlock):
    """SMC Mitigation Block."""
    pass
    
@dataclass(frozen=True)
class LiquiditySweep(ConceptObject):
    """SMC Liquidity Sweep Concept."""
    swept_liquidity_id: str = ""

@dataclass(frozen=True)
class TrendConcept(ConceptObject):
    """Semantic concept of a trend (bullish/bearish)."""
    trend_strength: float = 0.0
    duration_bars: int = 0
    
@dataclass(frozen=True)
class MomentumConcept(ConceptObject):
    """Semantic concept of momentum."""
    momentum_value: float = 0.0
    is_accelerating: bool = False
    
@dataclass(frozen=True)
class ContinuationConcept(ConceptObject):
    """Semantic concept of trend continuation."""
    probability: float = 0.0

@dataclass(frozen=True)
class VolatilityConcept(ConceptObject):
    """Semantic concept of volatility."""
    volatility_level: float = 0.0
    is_expanding: bool = False
