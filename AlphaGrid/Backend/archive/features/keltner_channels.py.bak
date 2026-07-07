import numpy as np
import pandas as pd
import hashlib
import uuid
from Backend.dtos.features import FeatureDTO
from Backend.features.atr import ATRFeatureGenerator

class KeltnerChannelFeatureGenerator:
    def __init__(self, ema_period: int = 20, atr_period: int = 10, atr_multiplier: float = 2.0):
        self.ema_period = ema_period
        self.atr_period = atr_period
        self.atr_multiplier = atr_multiplier
        self.component_id = f"ftr-keltner-{ema_period}-{atr_period}-{atr_multiplier}"
        self.atr_gen = ATRFeatureGenerator(period=atr_period)
        
    def generate(self, data: pd.DataFrame, trace_id: str, correlation_id: str) -> FeatureDTO:
        if len(data) < max(self.ema_period, self.atr_period):
            raise ValueError("Insufficient data for Keltner Channels")
            
        close = data['close']
        ema = close.ewm(span=self.ema_period, adjust=False).mean()
        
        # Calculate ATR series natively instead of using DTO for the whole series
        high = data['high']
        low = data['low']
        close_prev = close.shift(1)
        tr = pd.concat([high - low, (high - close_prev).abs(), (low - close_prev).abs()], axis=1).max(axis=1)
        atr_series = tr.ewm(alpha=1/self.atr_period, min_periods=self.atr_period, adjust=False).mean()
        
        upper_band = ema + (self.atr_multiplier * atr_series)
        lower_band = ema - (self.atr_multiplier * atr_series)
        
        current_upper = float(upper_band.iloc[-1])
        current_lower = float(lower_band.iloc[-1])
        current_ema = float(ema.iloc[-1])
        
        payload = f"{current_ema}:{current_upper}:{current_lower}"
        payload_hash = hashlib.md5(payload.encode()).hexdigest()
        
        return FeatureDTO(
            id=f"{self.component_id}-{uuid.uuid4().hex[:8]}",
            schema_version="1.0.0",
            producer=self.component_id,
            trace_id=trace_id,
            correlation_id=correlation_id,
            fingerprint=f"kc-{self.ema_period}-{self.atr_period}-{self.atr_multiplier}",
            checksum=payload_hash,
            symbol=data.attrs.get('symbol', 'UNKNOWN'),
            timeframe=data.attrs.get('timeframe', 'UNKNOWN'),
            values={
                'middle_band': current_ema,
                'upper_band': current_upper,
                'lower_band': current_lower
            },
            lineage={'dependencies': ['ftr-ohlcv', f'ftr-atr-{self.atr_period}']}
        )
