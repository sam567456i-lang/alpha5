from dataclasses import dataclass
from Backend.core.evidence_dtos.base import BasePlatformObject

@dataclass
class BaseVolumeObject(BasePlatformObject):
    """
    Root base for Volume Analytics objects.
    Derives purely from OHLCV and mathematical logic.
    """
    volume_uuid: str = ""
    measured_volume: float = 0.0
    relative_volume_ratio: float = 0.0

# --- Volume Relational ---
@dataclass
class RelativeVolume(BaseVolumeObject): pass

@dataclass
class VolumeDivergence(BaseVolumeObject): pass

@dataclass
class VolumeQuality(BaseVolumeObject): pass

# --- Volume Extrema ---
@dataclass
class ClimaxVolume(BaseVolumeObject):
    """Statistically extreme volume (e.g. > 2.5 SD)."""
    standard_deviations: float = 0.0

@dataclass
class DryUpVolume(BaseVolumeObject):
    """Statistically suppressed volume (e.g. < -2.0 SD)."""
    standard_deviations: float = 0.0

# --- Volume Trend ---
@dataclass
class VolumeExpansion(BaseVolumeObject):
    """Sequential increase in volume."""
    consecutive_bars: int = 0

@dataclass
class VolumeContraction(BaseVolumeObject):
    """Sequential decrease in volume."""
    consecutive_bars: int = 0

# --- Volume Flow (Combined with Price Geometry) ---
@dataclass
class BuyingPressure(BaseVolumeObject):
    """High volume on a bar that closes near its high."""
    close_percentage: float = 0.0

@dataclass
class SellingPressure(BaseVolumeObject):
    """High volume on a bar that closes near its low."""
    close_percentage: float = 0.0

# --- Advanced Statistical Extensions ---
@dataclass
class VolumePercentile(BaseVolumeObject):
    """Volume ranked as a percentile against a rolling window."""
    percentile_rank: float = 0.0

@dataclass
class RollingVolumeStatistics(BaseVolumeObject):
    """Aggregated statistical snapshot (mean, median, variance)."""
    rolling_mean: float = 0.0
    rolling_variance: float = 0.0

@dataclass
class VolumeRegime(BaseVolumeObject):
    """High/Low volume structural regime."""
    regime_type: str = "NORMAL" # HIGH, LOW, NORMAL

@dataclass
class VolumeAcceleration(BaseVolumeObject):
    """Rate of change of volume expansion."""
    acceleration_rate: float = 0.0

@dataclass
class VolumeDeceleration(BaseVolumeObject):
    """Rate of change of volume contraction."""
    deceleration_rate: float = 0.0

@dataclass
class ParticipationRate(BaseVolumeObject):
    """Volume as a percentage of total session or aggregate volume."""
    participation_percentage: float = 0.0

@dataclass
class VolumeEfficiency(BaseVolumeObject):
    """Price movement achieved per unit of volume."""
    efficiency_score: float = 0.0

@dataclass
class VolumePersistence(BaseVolumeObject):
    """Duration a specific volume regime has maintained."""
    bars_maintained: int = 0
