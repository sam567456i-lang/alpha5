from dataclasses import dataclass, field
from typing import Optional
from Backend.core.evidence_dtos.base import BasePlatformObject

# --- Momentum Policies ---
@dataclass
class VelocityPolicy:
    lookback_window: int = 14

@dataclass
class MomentumPolicy:
    velocity_policy: VelocityPolicy = field(default_factory=VelocityPolicy)

# --- Momentum Measurements (Detached Math Components) ---
@dataclass
class VelocityMeasurement:
    """Rate of price change over T bars."""
    absolute_velocity: float = 0.0

@dataclass
class AccelerationMeasurement:
    """Rate of change of velocity."""
    acceleration: float = 0.0

@dataclass
class JerkMeasurement:
    """Third derivative (rate of change of acceleration)."""
    jerk: float = 0.0

@dataclass
class RateOfChangeMeasurement:
    """Percentage drift over T bars."""
    roc_percentage: float = 0.0

@dataclass
class MomentumPersistenceMeasurement:
    """Count of consecutive bars maintaining directional velocity."""
    consecutive_bars: int = 0

@dataclass
class MomentumExhaustionMeasurement:
    """Statistical divergence indicating velocity exhaustion."""
    exhaustion_score: float = 0.0

# --- Unified Momentum Object ---
@dataclass
class MomentumObject(BasePlatformObject):
    """
    Root base for Momentum physics.
    Exclusively aggregates mathematical measurements. NO semantic opinions.
    """
    momentum_uuid: str = ""
    
    velocity: Optional[VelocityMeasurement] = None
    acceleration: Optional[AccelerationMeasurement] = None
    jerk: Optional[JerkMeasurement] = None
    rate_of_change: Optional[RateOfChangeMeasurement] = None
    persistence: Optional[MomentumPersistenceMeasurement] = None
    exhaustion: Optional[MomentumExhaustionMeasurement] = None
