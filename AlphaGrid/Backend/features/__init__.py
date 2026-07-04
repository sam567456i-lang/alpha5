"""Features package."""

from .base import AbstractFeature
from .registry import FeatureRegistry
from .engine import FeatureEngine
from .cache import FeatureCache

# Old unmigrated features
from .momentum import ROCFeature, RSIFeature
from .volatility import RelativeVolumeFeature
from .adx import ADXFeature
from .cci import CCIFeature
from .donchian import Donchian20Feature
from .stochastic import StochasticFeature
from .supertrend import SuperTrendFeature
from .high_low_breakout import HighLowBreakoutFeatureGenerator
from .rsi import RSIFeatureGenerator
from .stochastic_generator import StochasticFeatureGenerator
from .support_resistance import SupportResistanceFeatureGenerator
from .volatility_breakout import VolatilityBreakoutFeatureGenerator
from .vwap import VWAPFeatureGenerator

# Migrated Generators
from .sma_generator import SMAFeatureGenerator
from .ema_generator import EMAFeatureGenerator
from .wma_generator import WMAFeatureGenerator
from .ma_cross_generator import MACrossFeatureGenerator
from .macd_generator import MACDFeatureGenerator
from .roc_generator import ROCFeatureGenerator
from .atr_generator import ATRFeatureGenerator
from .bollinger_generator import BollingerFeatureGenerator
from .keltner_generator import KeltnerFeatureGenerator

__all__ = [
    'AbstractFeature',
    'FeatureCache',
    'FeatureEngine',
    'FeatureRegistry',
    'ADXFeature',
    'Donchian20Feature',
    'HighLowBreakoutFeatureGenerator',
    'ROCFeature',
    'RSIFeature',
    'RSIFeatureGenerator',
    'RelativeVolumeFeature',
    'StochasticFeature',
    'StochasticFeatureGenerator',
    'SuperTrendFeature',
    'SupportResistanceFeatureGenerator',
    'VWAPFeatureGenerator',
    'VolatilityBreakoutFeatureGenerator',
    'CCIFeature',
    'SMAFeatureGenerator',
    'EMAFeatureGenerator',
    'WMAFeatureGenerator',
    'MACrossFeatureGenerator',
    'MACDFeatureGenerator',
    'ROCFeatureGenerator',
    'ATRFeatureGenerator',
    'BollingerFeatureGenerator',
    'KeltnerFeatureGenerator'
]
