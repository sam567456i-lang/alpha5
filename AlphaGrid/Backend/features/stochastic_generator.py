from __future__ import annotations
from typing import TYPE_CHECKING
import numpy as np
import pandas as pd
import hashlib
import uuid
from Backend.dtos.features import FeatureDTO

class StochasticFeatureGenerator:
    def __init__(self, k_period: int = 14, d_period: int = 3, smooth_k: int = 3):
        self.k_period = k_period
        self.d_period = d_period
        self.smooth_k = smooth_k
        self.component_id = f"ftr-stoch-{k_period}-{d_period}-{smooth_k}"
        
    def generate(self, data: pd.DataFrame, trace_id: str, correlation_id: str) -> FeatureDTO:
        if len(data) < self.k_period + max(self.smooth_k, self.d_period):
            raise ValueError(f"Insufficient data. Required: {self.k_period + max(self.smooth_k, self.d_period)}")
            
        low_min = data['low'].rolling(window=self.k_period).min()
        high_max = data['high'].rolling(window=self.k_period).max()
        
        # Fast %K
        fast_k = 100 * ((data['close'] - low_min) / (high_max - low_min))
        
        # Slow %K
        k_val = fast_k.rolling(window=self.smooth_k).mean()
        
        # %D
        d_val = k_val.rolling(window=self.d_period).mean()
        
        current_k = float(k_val.iloc[-1])
        current_d = float(d_val.iloc[-1])
        
        payload = f"{current_k}:{current_d}"
        payload_hash = hashlib.md5(payload.encode()).hexdigest()
        
        return FeatureDTO(
            id=f"{self.component_id}-{uuid.uuid4().hex[:8]}",
            schema_version="1.0.0",
            producer=self.component_id,
            trace_id=trace_id,
            correlation_id=correlation_id,
            fingerprint=f"stoch-{self.k_period}-{self.d_period}-{self.smooth_k}",
            checksum=payload_hash,
            symbol=data.attrs.get('symbol', 'UNKNOWN'),
            timeframe=data.attrs.get('timeframe', 'UNKNOWN'),
            values={'k': current_k, 'd': current_d},
            lineage={'dependencies': ['ftr-ohlcv']}
        )
