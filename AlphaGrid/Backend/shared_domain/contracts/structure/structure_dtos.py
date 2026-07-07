from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List, Dict, Any
from Backend.shared_domain.contracts.base.base_dtos import RegistryConceptDTO

class StructureClassificationDTO(Enum):
    OBJECT = "OBJECT"       # e.g., Swing Structure, Fractal
    EVENT = "EVENT"         # e.g., BOS, CHOCH, MSS
    CONTEXT = "CONTEXT"     # e.g., HTF Bias, Trend Phase

class StructureStateDTO(Enum):
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"
    CONSOLIDATION = "CONSOLIDATION"
    PULLBACK = "PULLBACK"
    EXPANSION = "EXPANSION"

@dataclass(frozen=True)
class StructureObjectDTO(RegistryConceptDTO):
    """
    Represents structural objects like Internal/External Structure, Swings.
    """
    classification: StructureClassificationDTO = field(default=StructureClassificationDTO.OBJECT, init=False)
    high_price: float
    low_price: float
    is_confirmed: bool
    structural_timeframe: str

@dataclass(frozen=True)
class StructureEventDTO(RegistryConceptDTO):
    """
    Represents structural events like BOS, CHOCH, MSS.
    """
    classification: StructureClassificationDTO = field(default=StructureClassificationDTO.EVENT, init=False)
    event_price: float
    breakout_volume: Optional[float] = None
    invalidated_object_id: Optional[str] = None
    is_internal: bool = False

@dataclass(frozen=True)
class StructureContextDTO(RegistryConceptDTO):
    """
    Represents structural context like HTF Bias, Trend Strength.
    """
    classification: StructureClassificationDTO = field(default=StructureClassificationDTO.CONTEXT, init=False)
    current_state: StructureStateDTO
    strength_score: float = 0.0
    aligned_timeframes: List[str] = field(default_factory=list)

@dataclass(frozen=True)
class StructureRelationshipDTO:
    """
    Represents relationships between structural components.
    """
    source_id: str
    target_id: str
    relationship_type: str # e.g., "INVALIDATES", "CONFIRMS", "PRECEDES"
    strength: float = 1.0
