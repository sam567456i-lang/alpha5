from __future__ import annotations
from typing import TYPE_CHECKING
import numpy as np
if TYPE_CHECKING:
    import pandas as pd
from typing import Dict, Any, TYPE_CHECKING, Optional, TYPE_CHECKING
from datetime import datetime
import hashlib
import uuid
from Backend.dtos.features import FeatureDTO

class RSIFeatureGenerator:
    def __init__(self, period: int = 14):
        self.period = period
        self.component_id = f"ftr-rsi-{period}"
        
    def generate(self, data: pd.DataFrame, trace_id: str, correlation_id: str) -> FeatureDTO:
        if len(data) < self.period + 1:
            raise ValueError(f"Insufficient data. Required: {self.period + 1}, Got: {len(data)}")
            
        close = data['close']
        delta = close.diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)
        
        # Wilder's Smoothing
        avg_gain = gain.ewm(alpha=1/self.period, min_periods=self.period, adjust=False).mean()
        avg_loss = loss.ewm(alpha=1/self.period, min_periods=self.period, adjust=False).mean()
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        current_rsi = float(rsi.iloc[-1])
        
        payload_hash = hashlib.md5(str(current_rsi).encode()).hexdigest()
        
        return FeatureDTO(
            id=f"{self.component_id}-{uuid.uuid4().hex[:8]}",
            schema_version="1.0.0",
            producer=self.component_id,
            trace_id=trace_id,
            correlation_id=correlation_id,
            fingerprint=f"rsi-{self.period}",
            checksum=payload_hash,
            symbol=data.attrs.get('symbol', 'UNKNOWN'),
            timeframe=data.attrs.get('timeframe', 'UNKNOWN'),
            values={'rsi': current_rsi},
            lineage={'dependencies': ['ftr-ohlcv']}
        )
