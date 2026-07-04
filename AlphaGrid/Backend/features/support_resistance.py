from __future__ import annotations
from typing import TYPE_CHECKING
import numpy as np
import pandas as pd
import hashlib
import uuid
from Backend.dtos.features import FeatureDTO


class SupportResistanceFeatureGenerator:
    """Identifies key support and resistance levels from rolling highs/lows."""

    component_metadata = {
        'consumes': ['MarketDataDTO (OHLCV)'],
        'produces': ['FeatureDTO'],
        'warmup': 'lookback',
        'complexity': 'O(n)',
        'memory': 'O(lookback)',
        'deterministic': True,
        'switch': 'breakout_family',
    }

    def __init__(self, lookback: int = 20):
        self.lookback = lookback
        self.component_id = f"ftr-sr-{lookback}"

    def generate(self, data: pd.DataFrame, trace_id: str, correlation_id: str) -> FeatureDTO:
        if len(data) < self.lookback:
            raise ValueError(f"Insufficient data. Required: {self.lookback}, Got: {len(data)}")

        resistance = float(data['high'].rolling(window=self.lookback).max().iloc[-1])
        support = float(data['low'].rolling(window=self.lookback).min().iloc[-1])
        current_close = float(data['close'].iloc[-1])

        # Distance from levels as a fraction of range
        sr_range = resistance - support
        distance_to_resistance = (resistance - current_close) / sr_range if sr_range > 0 else 0.0
        distance_to_support = (current_close - support) / sr_range if sr_range > 0 else 0.0

        payload = f"{resistance}:{support}:{distance_to_resistance}:{distance_to_support}"
        payload_hash = hashlib.md5(payload.encode()).hexdigest()

        return FeatureDTO(
            id=f"{self.component_id}-{uuid.uuid4().hex[:8]}",
            schema_version="1.0.0",
            producer=self.component_id,
            trace_id=trace_id,
            correlation_id=correlation_id,
            fingerprint=f"sr-{self.lookback}",
            checksum=payload_hash,
            symbol=data.attrs.get('symbol', 'UNKNOWN'),
            timeframe=data.attrs.get('timeframe', 'UNKNOWN'),
            values={
                'resistance': resistance,
                'support': support,
                'distance_to_resistance': distance_to_resistance,
                'distance_to_support': distance_to_support,
                'sr_range': sr_range,
            },
            lineage={'dependencies': ['ftr-ohlcv']}
        )
