from __future__ import annotations
from typing import TYPE_CHECKING
import numpy as np
import pandas as pd
import hashlib
import uuid
from Backend.dtos.features import FeatureDTO

class BollingerBandsFeatureGenerator:
    def __init__(self, period: int = 20, std_dev: float = 2.0):
        self.period = period
        self.std_dev = std_dev
        self.component_id = f"ftr-bollinger-{period}-{std_dev}"
        
    def generate(self, data: pd.DataFrame, trace_id: str, correlation_id: str) -> FeatureDTO:
        if len(data) < self.period:
            raise ValueError(f"Insufficient data. Required: {self.period}, Got: {len(data)}")
            
        close = data['close']
        sma = close.rolling(window=self.period).mean()
        std = close.rolling(window=self.period).std(ddof=0)
        
        upper_band = sma + (std * self.std_dev)
        lower_band = sma - (std * self.std_dev)
        
        current_upper = float(upper_band.iloc[-1])
        current_lower = float(lower_band.iloc[-1])
        current_sma = float(sma.iloc[-1])
        percent_b = float((close.iloc[-1] - current_lower) / (current_upper - current_lower)) if current_upper != current_lower else 0.5
        
        payload = f"{current_sma}:{current_upper}:{current_lower}"
        payload_hash = hashlib.md5(payload.encode()).hexdigest()
        
        return FeatureDTO(
            id=f"{self.component_id}-{uuid.uuid4().hex[:8]}",
            schema_version="1.0.0",
            producer=self.component_id,
            trace_id=trace_id,
            correlation_id=correlation_id,
            fingerprint=f"bb-{self.period}-{self.std_dev}",
            checksum=payload_hash,
            symbol=data.attrs.get('symbol', 'UNKNOWN'),
            timeframe=data.attrs.get('timeframe', 'UNKNOWN'),
            values={
                'middle_band': current_sma,
                'upper_band': current_upper,
                'lower_band': current_lower,
                'percent_b': percent_b
            },
            lineage={'dependencies': ['ftr-ohlcv']}
        )
