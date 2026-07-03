import numpy as np
import pandas as pd
import hashlib
import uuid
from Backend.dtos.features import FeatureDTO


class VolatilityBreakoutFeatureGenerator:
    """Detects breakout conditions when price exceeds ATR-based expansion thresholds."""

    component_metadata = {
        'consumes': ['MarketDataDTO (OHLCV)'],
        'produces': ['FeatureDTO'],
        'warmup': 'atr_period + 1',
        'complexity': 'O(n)',
        'memory': 'O(atr_period)',
        'deterministic': True,
        'switch': 'breakout_family',
    }

    def __init__(self, atr_period: int = 14, multiplier: float = 1.5):
        self.atr_period = atr_period
        self.multiplier = multiplier
        self.component_id = f"ftr-volbreakout-{atr_period}-{multiplier}"

    def generate(self, data: pd.DataFrame, trace_id: str, correlation_id: str) -> FeatureDTO:
        if len(data) < self.atr_period + 1:
            raise ValueError(f"Insufficient data. Required: {self.atr_period + 1}")

        high = data['high']
        low = data['low']
        close = data['close']
        close_prev = close.shift(1)

        tr = pd.concat([high - low, (high - close_prev).abs(), (low - close_prev).abs()], axis=1).max(axis=1)
        atr = tr.ewm(alpha=1 / self.atr_period, min_periods=self.atr_period, adjust=False).mean()

        current_atr = float(atr.iloc[-1])
        prev_close = float(close.iloc[-2])
        current_close = float(close.iloc[-1])

        upper_threshold = prev_close + (current_atr * self.multiplier)
        lower_threshold = prev_close - (current_atr * self.multiplier)

        upside_breakout = current_close > upper_threshold
        downside_breakout = current_close < lower_threshold

        payload = f"{upper_threshold}:{lower_threshold}:{upside_breakout}:{downside_breakout}"
        payload_hash = hashlib.md5(payload.encode()).hexdigest()

        return FeatureDTO(
            id=f"{self.component_id}-{uuid.uuid4().hex[:8]}",
            schema_version="1.0.0",
            producer=self.component_id,
            trace_id=trace_id,
            correlation_id=correlation_id,
            fingerprint=f"volbreakout-{self.atr_period}-{self.multiplier}",
            checksum=payload_hash,
            symbol=data.attrs.get('symbol', 'UNKNOWN'),
            timeframe=data.attrs.get('timeframe', 'UNKNOWN'),
            values={
                'atr': current_atr,
                'upper_threshold': upper_threshold,
                'lower_threshold': lower_threshold,
                'upside_breakout': upside_breakout,
                'downside_breakout': downside_breakout,
            },
            lineage={'dependencies': ['ftr-ohlcv', f'ftr-atr-{self.atr_period}']}
        )
