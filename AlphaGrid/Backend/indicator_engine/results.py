from dataclasses import dataclass
import numpy as np
from typing import Dict, Any, List

@dataclass(frozen=True)
class FinancialIndicatorResult:
    """Base class for all indicator engine results. Purely numerical."""
    timestamps: np.ndarray
    valid_mask: np.ndarray
    warmup_period: int
    lookback: int
    metadata: Dict[str, Any]
    
@dataclass(frozen=True)
class MACDResult(FinancialIndicatorResult):
    macd: np.ndarray
    signal: np.ndarray
    histogram: np.ndarray

@dataclass(frozen=True)
class ROCResult(FinancialIndicatorResult):
    roc: np.ndarray

@dataclass(frozen=True)
class SMAResult(FinancialIndicatorResult):
    sma: np.ndarray

@dataclass(frozen=True)
class EMAResult(FinancialIndicatorResult):
    ema: np.ndarray

@dataclass(frozen=True)
class WMAResult(FinancialIndicatorResult):
    wma: np.ndarray

@dataclass(frozen=True)
class MACrossResult(FinancialIndicatorResult):
    fast_ma: np.ndarray
    slow_ma: np.ndarray
    cross_signal: np.ndarray

@dataclass(frozen=True)
class ATRResult(FinancialIndicatorResult):
    atr: np.ndarray

@dataclass(frozen=True)
class BollingerResult(FinancialIndicatorResult):
    upper: np.ndarray
    middle: np.ndarray
    lower: np.ndarray
    bandwidth: np.ndarray
    percent_b: np.ndarray

@dataclass(frozen=True)
class KeltnerResult(FinancialIndicatorResult):
    upper: np.ndarray
    middle: np.ndarray
    lower: np.ndarray

@dataclass(frozen=True)
class DonchianResult(FinancialIndicatorResult):
    upper: np.ndarray
    lower: np.ndarray
    middle: np.ndarray
    bandwidth: np.ndarray

@dataclass(frozen=True)
class HighLowResult(FinancialIndicatorResult):
    highest_high: np.ndarray
    lowest_low: np.ndarray

@dataclass(frozen=True)
class SupportResistanceResult(FinancialIndicatorResult):
    resistance: np.ndarray
    support: np.ndarray
    distance_to_resistance: np.ndarray
    distance_to_support: np.ndarray

@dataclass(frozen=True)
class RSIResult(FinancialIndicatorResult):
    rsi: np.ndarray

@dataclass(frozen=True)
class VWAPResult(FinancialIndicatorResult):
    vwap: np.ndarray

@dataclass(frozen=True)
class RelativeVolumeResult(FinancialIndicatorResult):
    relative_volume: np.ndarray

@dataclass(frozen=True)
class OBVResult(FinancialIndicatorResult):
    obv: np.ndarray

@dataclass(frozen=True)
class VolumeSMAResult(FinancialIndicatorResult):
    volume_sma: np.ndarray

@dataclass(frozen=True)
class AccumulationDistributionResult(FinancialIndicatorResult):
    ad: np.ndarray
