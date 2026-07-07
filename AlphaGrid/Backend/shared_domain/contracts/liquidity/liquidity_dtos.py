from dataclasses import dataclass
from typing import Optional
from enum import Enum
from Backend.shared_domain.contracts.base.lineage import LineageDTO
from Backend.shared_domain.contracts.base.confidence import ConfidenceProfileDTO
from Backend.shared_domain.contracts.base.freshness import FreshnessProfileDTO
from Backend.shared_domain.contracts.base.identity import IdentityDTO

class LiquidityClassificationDTO(str, Enum):
    TIME_BASED = "TIME_BASED"
    SWING = "SWING"
    EQUAL = "EQUAL"
    SESSION = "SESSION"
    RANGE = "RANGE"
    TREND = "TREND"
    MISC = "MISC"

class LiquidityStrengthDTO(str, Enum):
    WEAK = "WEAK"
    MODERATE = "MODERATE"
    STRONG = "STRONG"
    MAJOR = "MAJOR"

@dataclass(frozen=True)
class LiquidityLevelDTO:
    price: float
    volume_at_level: Optional[float] = None
    touches: int = 1

@dataclass(frozen=True)
class LiquidityZoneDTO:
    high_price: float
    low_price: float
    is_mitigated: bool = False

@dataclass(frozen=True)
class LiquidityObjectDTO:
    """Master DTO for all Liquidity concepts (PDH, Swings, Sessions, etc.)"""
    identity: IdentityDTO
    classification: LiquidityClassificationDTO
    strength: LiquidityStrengthDTO
    level: Optional[LiquidityLevelDTO]
    zone: Optional[LiquidityZoneDTO]
    
    confidence: ConfidenceProfileDTO
    freshness: FreshnessProfileDTO
    lineage: Optional[LineageDTO] = None
