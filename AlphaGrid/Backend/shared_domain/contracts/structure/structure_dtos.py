from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List, Dict, Any
from datetime import datetime
from Backend.price_geometry.objects import Swing  # Formal swing ownership

class StructureClassificationDTO(Enum):
    OBJECT = "OBJECT"
    EVENT = "EVENT"
    CONTEXT = "CONTEXT"

class StructureStateDTO(Enum):
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"
    CONSOLIDATION = "CONSOLIDATION"
    PULLBACK = "PULLBACK"
    EXPANSION = "EXPANSION"
    UNKNOWN = "UNKNOWN"

@dataclass(frozen=True)
class StructureObjectDTO:
    """
    Represents structural objects.
    Must wrap/consume existing Geometry Swings rather than raw price.
    """
    id: str
    timestamp: datetime
    consumes: List[str]
    produces: List[str]
    classification: StructureClassificationDTO = field(default=StructureClassificationDTO.OBJECT, init=False)
    source_swing: Swing  # Mandated Swing Ownership
    is_confirmed: bool
    structural_timeframe: str

@dataclass(frozen=True)
class StructureEventDTO:
    """
    Represents structural events like BOS, CHOCH, MSS.
    """
    id: str
    timestamp: datetime
    consumes: List[str]
    produces: List[str]
    classification: StructureClassificationDTO = field(default=StructureClassificationDTO.EVENT, init=False)
    event_price: float
    sequence_number: int # For deterministic replay ordering
    breakout_volume: Optional[float] = None
    invalidated_object_id: Optional[str] = None
    is_internal: bool = False
    is_confirmed: bool = True # Differentiates confirmed vs tentative BOS

@dataclass(frozen=True)
class StructureStateIdentity:
    """
    Multi-Timeframe Isolation ID.
    State identity should be (market, asset_class, exchange, symbol, timeframe, session_id, data_feed)
    """
    market: str
    asset_class: str
    exchange: str
    symbol: str
    timeframe: str
    session_id: str
    data_feed: str

@dataclass(frozen=True)
class StructureContextDTO:
    """
    Represents structural context like HTF Bias, Trend Phase.
    """
    id: str
    timestamp: datetime
    consumes: List[str]
    produces: List[str]
    classification: StructureClassificationDTO = field(default=StructureClassificationDTO.CONTEXT, init=False)
    identity: StructureStateIdentity
    current_state: StructureStateDTO
    sequence_number: int
    last_updated_timestamp: datetime
    registry_checksum: str = ""
    state_machine_version: str = "1.0.0"
    strength_score: float = 0.0
    aligned_timeframes: List[str] = field(default_factory=list)

@dataclass(frozen=True)
class StructureRelationshipDTO:
    source_id: str
    target_id: str
    relationship_type: str
    strength: float = 1.0
