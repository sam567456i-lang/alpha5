from __future__ import annotations
from typing import TYPE_CHECKING
import numpy as np
import pandas as pd
import hashlib
import uuid
from Backend.dtos.features import FeatureDTO

class ATRFeatureGenerator:
    def __init__(self, period: int = 14):
        self.period = period
        self.component_id = f"ftr-atr-{period}"
        
    def generate(self, data: pd.DataFrame, trace_id: str, correlation_id: str) -> FeatureDTO:
        if len(data) < self.period:
            raise ValueError(f"Insufficient data. Required: {self.period}")
            
        high = data['high']
        low = data['low']
        close_prev = data['close'].shift(1)
        
        tr1 = high - low
        tr2 = (high - close_prev).abs()
        tr3 = (low - close_prev).abs()
        
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        # Wilder's Smoothing for ATR
        atr = tr.ewm(alpha=1/self.period, min_periods=self.period, adjust=False).mean()
        
        current_atr = float(atr.iloc[-1])
        payload = str(current_atr)
        payload_hash = hashlib.md5(payload.encode()).hexdigest()
        
        return FeatureDTO(
            id=f"{self.component_id}-{uuid.uuid4().hex[:8]}",
            schema_version="1.0.0",
            producer=self.component_id,
            trace_id=trace_id,
            correlation_id=correlation_id,
            fingerprint=f"atr-{self.period}",
            checksum=payload_hash,
            symbol=data.attrs.get('symbol', 'UNKNOWN'),
            timeframe=data.attrs.get('timeframe', 'UNKNOWN'),
            values={'atr': current_atr},
            lineage={'dependencies': ['ftr-ohlcv']}
        )
