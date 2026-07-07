import numpy as np
import pandas as pd
import hashlib
import uuid
from Backend.dtos.features import FeatureDTO


class HighLowBreakoutFeatureGenerator:
    """Detects N-period high/low breakout conditions."""

    component_metadata = {
        'consumes': ['MarketDataDTO (OHLCV)'],
        'produces': ['FeatureDTO'],
        'warmup': 'period + 1',
        'complexity': 'O(n)',
        'memory': 'O(period)',
        'deterministic': True,
        'switch': 'breakout_family',
    }

    def __init__(self, period: int = 20):
        self.period = period
        self.component_id = f"ftr-hlbreakout-{period}"

    def generate(self, data: pd.DataFrame, trace_id: str, correlation_id: str) -> FeatureDTO:
        if len(data) < self.period + 1:
            raise ValueError(f"Insufficient data. Required: {self.period + 1}, Got: {len(data)}")

        # Lookback excludes current bar
        lookback_high = float(data['high'].iloc[-(self.period + 1):-1].max())
        lookback_low = float(data['low'].iloc[-(self.period + 1):-1].min())
        current_close = float(data['close'].iloc[-1])

        high_breakout = current_close > lookback_high
        low_breakout = current_close < lookback_low

        payload = f"{lookback_high}:{lookback_low}:{current_close}:{high_breakout}:{low_breakout}"
        payload_hash = hashlib.md5(payload.encode()).hexdigest()

        return FeatureDTO(
            id=f"{self.component_id}-{uuid.uuid4().hex[:8]}",
            schema_version="1.0.0",
            producer=self.component_id,
            trace_id=trace_id,
            correlation_id=correlation_id,
            fingerprint=f"hlbreakout-{self.period}",
            checksum=payload_hash,
            symbol=data.attrs.get('symbol', 'UNKNOWN'),
            timeframe=data.attrs.get('timeframe', 'UNKNOWN'),
            values={
                'lookback_high': lookback_high,
                'lookback_low': lookback_low,
                'high_breakout': high_breakout,
                'low_breakout': low_breakout,
            },
            lineage={'dependencies': ['ftr-ohlcv']}
        )
