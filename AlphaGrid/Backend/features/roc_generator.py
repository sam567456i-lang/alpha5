from __future__ import annotations
from typing import TYPE_CHECKING
import numpy as np
if TYPE_CHECKING:
    import pandas as pd
import hashlib
import uuid
from typing import Dict, Any, TYPE_CHECKING, Optional, TYPE_CHECKING
from Backend.dtos.features import FeatureDTO
from Backend.features.interfaces.momentum_feature import MomentumFeatureInterface

class ROCFeatureGenerator(MomentumFeatureInterface):
    """
    Canonical Production Rate of Change (ROC) Generator.
    Produces generic momentum semantics.
    """
    def __init__(self, period: int = 14):
        self.period = period
        self._component_id = f"ftr-roc-{period}"
        
    @property
    def component_id(self) -> str:
        return self._component_id
        
    def generate(self, data: pd.DataFrame, trace_id: str, correlation_id: str) -> FeatureDTO:
        if len(data) < self.period + 1:
            raise ValueError(f"Insufficient data. Required: {self.period + 1}")
            
        close = data['close']
        roc = ((close - close.shift(self.period)) / close.shift(self.period)) * 100
        
        current_roc = float(roc.iloc[-1])
        prev_roc = float(roc.iloc[-2]) if len(roc) > 1 else 0.0
        
        # Generic Semantics
        momentum_strength = abs(current_roc)
        momentum_direction = 1.0 if current_roc > 0 else -1.0
        momentum_acceleration = current_roc - prev_roc
        
        payload_hash = hashlib.md5(f"{current_roc}".encode()).hexdigest()
        
        return FeatureDTO(
            id=f"{self.component_id}-{uuid.uuid4().hex[:8]}",
            schema_version="1.0.0",
            producer=self.component_id,
            trace_id=trace_id,
            correlation_id=correlation_id,
            fingerprint=f"roc-{self.period}",
            checksum=payload_hash,
            symbol=data.attrs.get('symbol', 'UNKNOWN'),
            timeframe=data.attrs.get('timeframe', 'UNKNOWN'),
            values={
                'roc': current_roc,
                'momentum_strength': momentum_strength,
                'momentum_direction': momentum_direction,
                'momentum_acceleration': momentum_acceleration
            },
            metadata={
                'feature_type': 'momentum',
                'indicator_family': 'roc',
                'lookback': self.period + 1,
                'warmup': self.period + 1,
                'lag': 'low',
                'complexity': 'O(n)',
                'memory_class': 'O(period)',
                'deterministic': True,
                'numeric_stability': 'medium' # Sensitive to gaps
            },
            lineage={'dependencies': ['ftr-ohlcv']}
        )
