from dataclasses import dataclass, field
from enum import Enum
from typing import List
from Backend.core.evidence_dtos.base import BasePlatformObject, ObjectRelationship

class ZoneValidity(Enum):
    VALID = "VALID"
    INVALIDATED = "INVALIDATED"

class ZoneFreshness(Enum):
    FRESH = "FRESH"
    TESTED = "TESTED"
    MITIGATED = "MITIGATED"

class MitigationState(Enum):
    UNMITIGATED = "UNMITIGATED"
    PARTIAL = "PARTIAL"
    FULL = "FULL"

@dataclass
class BaseInstitutionalZone(BasePlatformObject):
    """
    Root base class for all Institutional Zones.
    Must natively consume prior Structure Events and Liquidity Objects.
    """
    zone_uuid: str = ""
    upper_boundary_uuid: str = ""
    lower_boundary_uuid: str = ""
    origin_structure_uuids: List[str] = field(default_factory=list)
    origin_event_uuids: List[str] = field(default_factory=list)
    origin_liquidity_uuids: List[str] = field(default_factory=list)
    validity: ZoneValidity = ZoneValidity.VALID
    freshness: ZoneFreshness = ZoneFreshness.FRESH
    mitigation_state: MitigationState = MitigationState.UNMITIGATED

# --- Order Block Family ---
@dataclass
class OrderBlock(BaseInstitutionalZone): pass

@dataclass
class BullishOrderBlock(OrderBlock): pass

@dataclass
class BearishOrderBlock(OrderBlock): pass

# --- Breaker Family ---
@dataclass
class BreakerBlock(BaseInstitutionalZone): pass

@dataclass
class BullishBreaker(BreakerBlock): pass

@dataclass
class BearishBreaker(BreakerBlock): pass

# --- Mitigation Family ---
@dataclass
class MitigationBlock(BaseInstitutionalZone): pass

@dataclass
class BullishMitigation(MitigationBlock): pass

@dataclass
class BearishMitigation(MitigationBlock): pass

# --- Flip Zones ---
@dataclass
class FlipZone(BaseInstitutionalZone): pass

@dataclass
class SupportFlip(FlipZone): pass

@dataclass
class ResistanceFlip(FlipZone): pass

# --- Supply/Demand ---
@dataclass
class SupplyZone(BaseInstitutionalZone): pass

@dataclass
class DemandZone(BaseInstitutionalZone): pass

# --- Institutional Base ---
@dataclass
class InstitutionalBase(BaseInstitutionalZone): pass

@dataclass
class DecisionZone(InstitutionalBase): pass

@dataclass
class RallyBase(InstitutionalBase): pass

@dataclass
class DropBase(InstitutionalBase): pass
