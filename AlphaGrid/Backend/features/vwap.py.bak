import numpy as np
import pandas as pd
import hashlib
import uuid
from Backend.dtos.features import FeatureDTO

class VWAPFeatureGenerator:
    def __init__(self):
        self.component_id = "ftr-vwap"
        
    def generate(self, data: pd.DataFrame, trace_id: str, correlation_id: str) -> FeatureDTO:
        if len(data) < 1 or 'volume' not in data.columns:
            raise ValueError("Insufficient data or missing volume column for VWAP")
            
        # Assuming data is pre-sliced for the current session/day
        typical_price = (data['high'] + data['low'] + data['close']) / 3
        volume = data['volume']
        
        vwap_series = (typical_price * volume).cumsum() / volume.cumsum()
        current_vwap = float(vwap_series.iloc[-1])
        
        payload = str(current_vwap)
        payload_hash = hashlib.md5(payload.encode()).hexdigest()
        
        return FeatureDTO(
            id=f"{self.component_id}-{uuid.uuid4().hex[:8]}",
            schema_version="1.0.0",
            producer=self.component_id,
            trace_id=trace_id,
            correlation_id=correlation_id,
            fingerprint="vwap-session",
            checksum=payload_hash,
            symbol=data.attrs.get('symbol', 'UNKNOWN'),
            timeframe=data.attrs.get('timeframe', 'UNKNOWN'),
            values={'vwap': current_vwap},
            lineage={'dependencies': ['ftr-ohlcv']}
        )
