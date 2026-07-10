from dataclasses import dataclass
from typing import Optional
from enum import Enum
from Backend.core.evidence_dtos.base import BasePlatformEvent

class TransitionDirection(Enum):
    ASCENDING = "ASCENDING"
    DESCENDING = "DESCENDING"
    LATERAL = "LATERAL"

class ConfirmationStatus(Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    FAILED = "FAILED"

@dataclass
class StructureTransitionEvent(BasePlatformEvent):
    """
    Universal abstraction for all structural changes (BOS, CHOCH, MSS, etc).
    """
    previous_structure_uuid: str = ""
    next_structure_uuid: Optional[str] = None
    triggering_leg_uuid: str = ""
    triggering_boundary_uuid: str = ""
    triggering_price: float = 0.0
    transition_direction: TransitionDirection = TransitionDirection.LATERAL
    transition_strength: float = 0.0
    transition_quality: str = "STANDARD"
    confirmation_status: ConfirmationStatus = ConfirmationStatus.PENDING

# --- Break Events ---

@dataclass
class BOSEvent(StructureTransitionEvent): pass

@dataclass
class InternalBOSEvent(StructureTransitionEvent): pass

@dataclass
class ExternalBOSEvent(StructureTransitionEvent): pass

@dataclass
class FailedBOSEvent(StructureTransitionEvent): pass

@dataclass
class FakeBOSEvent(StructureTransitionEvent): pass

# --- Transition Events ---

@dataclass
class CHOCHEvent(StructureTransitionEvent): pass

@dataclass
class MSSEvent(StructureTransitionEvent): pass

@dataclass
class TrendTransitionEvent(StructureTransitionEvent): pass

@dataclass
class StructureFailureEvent(StructureTransitionEvent): pass

@dataclass
class StructureRecoveryEvent(StructureTransitionEvent): pass

# --- Validation Events ---

@dataclass
class BreakConfirmationEvent(StructureTransitionEvent): pass

@dataclass
class RetestEvent(StructureTransitionEvent): pass

@dataclass
class FailedRetestEvent(StructureTransitionEvent): pass

@dataclass
class AcceptanceEvent(StructureTransitionEvent): pass

@dataclass
class RejectionEvent(StructureTransitionEvent): pass

# --- Continuation Events ---

@dataclass
class ContinuationBreakEvent(StructureTransitionEvent): pass

@dataclass
class ExpansionEvent(StructureTransitionEvent): pass

@dataclass
class CompressionEvent(StructureTransitionEvent): pass

@dataclass
class LegExtensionEvent(StructureTransitionEvent): pass

@dataclass
class LegFailureEvent(StructureTransitionEvent): pass
