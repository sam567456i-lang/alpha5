from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class DistributionEvidence:
    asset: str
    timeframe: str
    timestamp: int
    mean: float
    variance: float
    skewness: float
    kurtosis: float
    entropy: float

@dataclass(frozen=True)
class RollingStatisticsEvidence:
    asset: str
    timeframe: str
    timestamp: int
    window_size: int
    rolling_mean: float
    rolling_variance: float
    rolling_std_dev: float

@dataclass(frozen=True)
class VolatilityEvidence:
    asset: str
    timeframe: str
    timestamp: int
    true_range: float
    atr: float
    historical_volatility: float
    parkinson_volatility: float
    garman_klass_volatility: float
    volatility_regime: str  # "Expanding", "Contracting", "Stable"

@dataclass(frozen=True)
class NormalizationEvidence:
    asset: str
    timeframe: str
    timestamp: int
    z_score: float
    robust_z_score: float
    percentile_rank: float
    min_max_normalized: float

@dataclass(frozen=True)
class ConfidenceEvidence:
    asset: str
    timeframe: str
    timestamp: int
    confidence_interval_upper: float
    confidence_interval_lower: float
    confidence_band_width: float

@dataclass(frozen=True)
class DriftEvidence:
    asset: str
    timeframe: str
    timestamp: int
    distribution_drift: float
    variance_drift: float

@dataclass(frozen=True)
class QualityEvidence:
    asset: str
    timeframe: str
    timestamp: int
    stationarity_score: float
    missing_data_ratio: float
