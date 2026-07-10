from dataclasses import dataclass, field
from Backend.core.evidence_dtos.base import BasePlatformEvent

@dataclass
class LiquidityEventObject(BasePlatformEvent):
    """
    Root event for interactions with Liquidity Pools, Reference Levels, and Session Boundaries.
    """
    pass

@dataclass
class SweepEvent(LiquidityEventObject):
    """Price pierces a liquidity level and then rapidly reverses."""
    pass

@dataclass
class TouchEvent(LiquidityEventObject):
    """Price tests a liquidity level exactly without breaching."""
    pass

@dataclass
class BreakEvent(LiquidityEventObject):
    """Price breaches a liquidity level with momentum/closing beyond it."""
    pass

@dataclass
class RejectEvent(LiquidityEventObject):
    """Price approaches a liquidity level and reverses before touching it."""
    pass

@dataclass
class ConsumeEvent(LiquidityEventObject):
    """Liquidity is completely absorbed and structurally invalidated."""
    pass

@dataclass
class RetestEvent(LiquidityEventObject):
    """Price returns to a previously broken liquidity level."""
    pass
