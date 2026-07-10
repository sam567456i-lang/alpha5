from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from Backend.core.evidence_dtos.base import BasePlatformObject

class ReferenceSource(Enum):
    CALENDAR = "CALENDAR"
    SESSION = "SESSION"
    RANGE = "RANGE"
    CUSTOM = "CUSTOM"

class ReferenceType(Enum):
    # Calendar types
    PREVIOUS_DAY_HIGH = "PREVIOUS_DAY_HIGH"
    PREVIOUS_DAY_LOW = "PREVIOUS_DAY_LOW"
    PREVIOUS_WEEK_HIGH = "PREVIOUS_WEEK_HIGH"
    PREVIOUS_WEEK_LOW = "PREVIOUS_WEEK_LOW"
    PREVIOUS_MONTH_HIGH = "PREVIOUS_MONTH_HIGH"
    PREVIOUS_MONTH_LOW = "PREVIOUS_MONTH_LOW"
    CURRENT_DAY_HIGH = "CURRENT_DAY_HIGH"
    CURRENT_DAY_LOW = "CURRENT_DAY_LOW"
    CURRENT_WEEK_HIGH = "CURRENT_WEEK_HIGH"
    CURRENT_WEEK_LOW = "CURRENT_WEEK_LOW"
    CURRENT_MONTH_HIGH = "CURRENT_MONTH_HIGH"
    CURRENT_MONTH_LOW = "CURRENT_MONTH_LOW"
    DAILY_OPEN = "DAILY_OPEN"
    WEEKLY_OPEN = "WEEKLY_OPEN"
    MONTHLY_OPEN = "MONTHLY_OPEN"
    MIDNIGHT_OPEN = "MIDNIGHT_OPEN"
    
    # Range types
    OPENING_RANGE_HIGH = "OPENING_RANGE_HIGH"
    OPENING_RANGE_LOW = "OPENING_RANGE_LOW"
    
    # Generic Custom Type
    CUSTOM = "CUSTOM"

@dataclass
class ReferenceLevel(BasePlatformObject):
    """
    A deterministic price level based on time or session geometry.
    Inherits identity, lineage, lifecycle state, quality, and relationships from BasePlatformObject.
    """
    reference_source: ReferenceSource = ReferenceSource.CALENDAR
    reference_type: ReferenceType = ReferenceType.CUSTOM
    price: float = 0.0
    
    # The timeframe interval this reference belongs to (if applicable)
    # e.g., '2026-07-08' for a Previous Day High of July 9th
    interval_identifier: str = ""

@dataclass(frozen=True)
class SwingLiquidityEvidence:
    """Distinct, immutable measurement component specific to Swing Liquidity."""
    price: float
    tolerance: float
    hierarchy_level: int
    source_swing_uuid: str

@dataclass
class SwingLiquidityObject(BasePlatformObject):
    """
    Aggregates Identity, Evidence, Quality, Lifecycle, Lineage, and Relationships.
    Inherits the standard BasePlatformObject fields and adds domain-specific evidence.
    """
    evidence: Optional[SwingLiquidityEvidence] = None

    def touch(self, lifecycle_engine):
        """Exposed hook for Wave 1.6 Liquidity Events."""
        from Backend.core.engines.lifecycle import LifecycleEvent
        lifecycle_engine.process_event(self, LifecycleEvent.TOUCH_REQUESTED)
        
    def break_level(self, lifecycle_engine):
        """Exposed hook for Wave 1.6 Liquidity Events."""
        # Break logic could be custom, e.g., moving to CONSUMED
        pass
        
    def consume(self, lifecycle_engine):
        """Exposed hook for Wave 1.6 Liquidity Events."""
        from Backend.core.engines.lifecycle import LifecycleEvent
        lifecycle_engine.process_event(self, LifecycleEvent.CONSUME_REQUESTED)

