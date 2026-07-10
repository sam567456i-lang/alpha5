from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any
from Backend.core.evidence_dtos.base import BasePlatformEvent

class TriggerSource(Enum):
    OHLC = "OHLC"
    TICK = "TICK"
    VOLUME = "VOLUME"
    REPLAY = "REPLAY"
    HISTORICAL_IMPORT = "HISTORICAL_IMPORT"

@dataclass
class BaseImbalanceEvent(BasePlatformEvent):
    """
    Universal Base for Imbalance Events (FirstTouch, PartialFill, etc.)
    Strictly answers "What happened?" without mutating state.
    """
    imbalance_uuid: str = ""
    trigger_source: TriggerSource = TriggerSource.OHLC
    trigger_revisions: Dict[str, str] = field(default_factory=dict) # e.g. {"object_rev": "1.0", "schema": "1.1"}
    measured_price: float = 0.0

# --- Contact Events ---
@dataclass
class FirstTouchEvent(BaseImbalanceEvent): pass

@dataclass
class ReTouchEvent(BaseImbalanceEvent): pass

@dataclass
class ExitEvent(BaseImbalanceEvent): pass

# --- Penetration Events ---
@dataclass
class PartialFillEvent(BaseImbalanceEvent):
    fill_percent_observed: float = 0.0
    penetration_depth_observed: float = 0.0

@dataclass
class DeepPenetrationEvent(PartialFillEvent): pass

@dataclass
class FullFillEvent(BaseImbalanceEvent): pass

# --- Structural Events ---
@dataclass
class MergeEvent(BaseImbalanceEvent): pass

@dataclass
class SplitEvent(BaseImbalanceEvent): pass

@dataclass
class ExpansionEvent(BaseImbalanceEvent): pass

@dataclass
class ContractionEvent(BaseImbalanceEvent): pass

# --- Lifecycle Events ---
@dataclass
class ActivatedEvent(BaseImbalanceEvent): pass

@dataclass
class InvalidatedEvent(BaseImbalanceEvent): pass

@dataclass
class ArchivedEvent(BaseImbalanceEvent): pass

# --- Relationship Events ---
@dataclass
class OverlapDetectedEvent(BaseImbalanceEvent): pass

@dataclass
class ClusterCreatedEvent(BaseImbalanceEvent): pass

@dataclass
class CompositeCreatedEvent(BaseImbalanceEvent): pass
