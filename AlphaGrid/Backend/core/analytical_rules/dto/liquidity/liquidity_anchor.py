from dataclasses import dataclass
from abc import ABC

@dataclass(frozen=True)
class LiquidityAnchor(ABC):
    """
    Base DTO for any price level capable of harboring liquidity.
    Normalizes Swings, Session Highs, Range bounds, etc.
    """
    anchor_id: str
    price: float
    timestamp: str
    origin_type: str # e.g., 'NODE_STRUCTURE_SWING_HIGH', 'NODE_SESSION_LOW' (Registry IDs)
    source_detector: str
    source_policy: str
    source_event: str
    origin_graph_namespace: str

@dataclass(frozen=True)
class SwingAnchor(LiquidityAnchor):
    """
    Implementation of LiquidityAnchor that wraps structural swings.
    """
    swing_id: str
