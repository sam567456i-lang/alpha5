from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List
from Backend.core.evidence_dtos.base import BasePlatformObject, BasePlatformEvent

class TradeClassificationRule(Enum):
    LEE_READY = "LEE_READY"
    TICK_RULE = "TICK_RULE"
    BID_ASK = "BID_ASK"
    EXCHANGE_NATIVE = "EXCHANGE_NATIVE"

@dataclass(frozen=True)
class TradeClassificationPolicy:
    rule: TradeClassificationRule = TradeClassificationRule.TICK_RULE

# --- Quality Metrics ---
@dataclass(frozen=True)
class OrderFlowQuality:
    trade_classification_confidence: float
    quote_completeness: float
    book_depth_quality: float
    timestamp_accuracy: float
    feed_consistency: float

# --- Measurements ---
@dataclass
class OrderFlowMeasurement(BasePlatformObject):
    """Abstract base for continuous numerical streams (not sparse objects)."""
    quality: OrderFlowQuality = None

@dataclass
class DeltaMeasurement(OrderFlowMeasurement):
    bid_volume: float = 0.0
    ask_volume: float = 0.0
    net_delta: float = 0.0

@dataclass
class CumulativeDeltaMeasurement(OrderFlowMeasurement):
    cvd: float = 0.0

# --- Objects ---
@dataclass
class OrderFlowObject(BasePlatformObject):
    """Sparse structural objects detected in the flow."""
    pass

@dataclass
class Absorption(OrderFlowObject):
    price_level: float = 0.0
    absorbed_volume: float = 0.0
    is_bid_absorption: bool = True # Bids absorbing aggressive sellers

@dataclass
class Iceberg(OrderFlowObject):
    price_level: float = 0.0
    estimated_hidden_size: float = 0.0
    is_bid_iceberg: bool = True

@dataclass
class Footprint(OrderFlowObject):
    price_levels: Dict[float, Dict[str, float]] = field(default_factory=dict) # price -> {'bid': vol, 'ask': vol}

# --- Events ---
@dataclass
class AbsorptionDetected(BasePlatformEvent):
    absorption_price: float = 0.0
