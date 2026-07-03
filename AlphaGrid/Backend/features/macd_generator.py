import numpy as np
import pandas as pd
import hashlib
import uuid
from typing import Dict, Any, Optional
from Backend.dtos.features import FeatureDTO
from Backend.features.interfaces.momentum_feature import MomentumFeatureInterface

class MACDFeatureGenerator(MomentumFeatureInterface):
    """
    Canonical Production MACD Generator.
    Produces both standard MACD outputs and generic momentum semantics.
    """
    def __init__(self, fast_period: int = 12, slow_period: int = 26, signal_period: int = 9):
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.signal_period = signal_period
        self._component_id = f"ftr-macd-{fast_period}-{slow_period}-{signal_period}"
        
    @property
    def component_id(self) -> str:
        return self._component_id
        
    def generate(self, data: pd.DataFrame, trace_id: str, correlation_id: str) -> FeatureDTO:
        if len(data) < self.slow_period + self.signal_period:
            raise ValueError(f"Insufficient data. Required: {self.slow_period + self.signal_period}")
            
        close = data['close']
        fast_ema = close.ewm(span=self.fast_period, adjust=False).mean()
        slow_ema = close.ewm(span=self.slow_period, adjust=False).mean()
        
        macd_line = fast_ema - slow_ema
        signal_line = macd_line.ewm(span=self.signal_period, adjust=False).mean()
        macd_histogram = macd_line - signal_line
        
        current_macd = float(macd_line.iloc[-1])
        current_signal = float(signal_line.iloc[-1])
        current_hist = float(macd_histogram.iloc[-1])
        prev_hist = float(macd_histogram.iloc[-2]) if len(macd_histogram) > 1 else 0.0
        
        # Generic Semantics
        momentum_strength = abs(current_macd)
        momentum_direction = 1.0 if current_macd > 0 else -1.0
        momentum_acceleration = current_hist - prev_hist
        
        payload_hash = hashlib.md5(f"{current_macd}{current_signal}{current_hist}".encode()).hexdigest()
        
        return FeatureDTO(
            id=f"{self.component_id}-{uuid.uuid4().hex[:8]}",
            schema_version="1.0.0",
            producer=self.component_id,
            trace_id=trace_id,
            correlation_id=correlation_id,
            fingerprint=f"macd-{self.fast_period}-{self.slow_period}-{self.signal_period}",
            checksum=payload_hash,
            symbol=data.attrs.get('symbol', 'UNKNOWN'),
            timeframe=data.attrs.get('timeframe', 'UNKNOWN'),
            values={
                'macd_line': current_macd,
                'signal_line': current_signal,
                'histogram': current_hist,
                'momentum_strength': momentum_strength,
                'momentum_direction': momentum_direction,
                'momentum_acceleration': momentum_acceleration
            },
            metadata={
                'feature_type': 'momentum',
                'indicator_family': 'macd',
                'lookback': self.slow_period + self.signal_period,
                'warmup': self.slow_period + self.signal_period,
                'lag': 'medium',
                'complexity': 'O(n)',
                'memory_class': 'O(period)',
                'deterministic': True,
                'numeric_stability': 'high'
            },
            lineage={'dependencies': ['ftr-ohlcv']}
        )
