from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class TrendDirectionEvidence:
    asset: str
    timeframe: str
    timestamp: int
    direction: str  # "Up", "Down", "Neutral"
    raw_slope: float

@dataclass(frozen=True)
class TrendStrengthEvidence:
    asset: str
    timeframe: str
    timestamp: int
    strength_classification: str  # "Weak", "Moderate", "Strong"
    raw_strength_score: float

@dataclass(frozen=True)
class TrendSlopeEvidence:
    asset: str
    timeframe: str
    timestamp: int
    slope: float
    slope_angle_degrees: float

@dataclass(frozen=True)
class TrendAccelerationEvidence:
    asset: str
    timeframe: str
    timestamp: int
    acceleration: float

@dataclass(frozen=True)
class TrendStateEvidence:
    asset: str
    timeframe: str
    timestamp: int
    state: str  # "Impulse", "Correction", "Expansion", "Compression", "Consolidation", "Transition"

@dataclass(frozen=True)
class TrendPersistenceEvidence:
    asset: str
    timeframe: str
    timestamp: int
    persistence_classification: str  # "Increasing", "Stable", "Weakening"
    duration_bars: int

@dataclass(frozen=True)
class TrendHierarchyEvidence:
    asset: str
    timeframe: str
    timestamp: int
    alignment: float  # -1.0 to 1.0 representing alignment with higher timeframes

@dataclass(frozen=True)
class TrendConfidenceEvidence:
    asset: str
    timeframe: str
    timestamp: int
    confidence_score: float  # 0.0 to 1.0

@dataclass(frozen=True)
class TrendConsistencyEvidence:
    asset: str
    timeframe: str
    timestamp: int
    consistency_ratio: float

@dataclass(frozen=True)
class TrendQualityEvidence:
    asset: str
    timeframe: str
    timestamp: int
    signal_to_noise_ratio: float
