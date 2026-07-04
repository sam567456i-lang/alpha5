from __future__ import annotations
from typing import TYPE_CHECKING
import numpy as np
if TYPE_CHECKING:
    import pandas as pd
import hashlib
import uuid
from typing import Dict, Any, Optional
from Backend.dtos.features import FeatureDTO
from Backend.features.interfaces.trend_feature import TrendFeatureInterface
from Backend.indicator_engine.runner import IndicatorRunner
from Backend.market_data.market_series import MarketSeries

class MACrossFeatureGenerator(TrendFeatureInterface):
    """
    Canonical Production MA Cross Generator.
    Delegates numerical composition strictly to the Indicator Engine.
    """
    def __init__(self, fast_period: int = 10, slow_period: int = 30, fast_type: str = "ema", slow_type: str = "ema"):
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.fast_type = fast_type
        self.slow_type = slow_type
        self._component_id = f"ftr-ma-cross-{fast_type}{fast_period}-{slow_type}{slow_period}"
        
    @property
    def component_id(self) -> str:
        return self._component_id
        
    def generate(self, data: pd.DataFrame, trace_id: str, correlation_id: str) -> FeatureDTO:
        req_len = max(self.fast_period, self.slow_period)
        if len(data) < req_len:
            raise ValueError(f"Insufficient data. Required: {req_len}")
            
        timestamps = data.index.astype(np.int64).values // 10**9 if hasattr(data.index, 'astype') else np.arange(len(data))
        series = MarketSeries(
            symbol=data.attrs.get('symbol', 'UNKNOWN'),
            timeframe=data.attrs.get('timeframe', 'UNKNOWN'),
            timestamps=timestamps,
            opens=data['open'].values if 'open' in data else np.zeros(len(data)),
            highs=data['high'].values if 'high' in data else np.zeros(len(data)),
            lows=data['low'].values if 'low' in data else np.zeros(len(data)),
            closes=data['close'].values,
            volumes=data['volume'].values if 'volume' in data else np.zeros(len(data))
        )
        
        cross_res = IndicatorRunner.execute(
            indicator_id="ma_cross",
            series=series,
            fast_period=self.fast_period,
            slow_period=self.slow_period,
            fast_type=self.fast_type,
            slow_type=self.slow_type
        )
        
        if not cross_res.valid_mask[-1]:
            current_fast = float('nan')
            current_slow = float('nan')
            current_cross = float('nan')
        else:
            current_fast = float(cross_res.fast_ma[-1])
            current_slow = float(cross_res.slow_ma[-1])
            current_cross = float(cross_res.cross_signal[-1])
        
        safe_payload = f"{'NaN' if np.isnan(current_cross) else current_cross}"
        payload_hash = hashlib.md5(safe_payload.encode()).hexdigest()
        
        return FeatureDTO(
            id=f"{self.component_id}-{uuid.uuid4().hex[:8]}",
            schema_version="1.0.0",
            producer=self.component_id,
            trace_id=trace_id,
            correlation_id=correlation_id,
            fingerprint=f"ma-cross-{self.fast_type}{self.fast_period}-{self.slow_type}{self.slow_period}",
            checksum=payload_hash,
            symbol=series.symbol,
            timeframe=series.timeframe,
            values={
                'fast_ma': current_fast,
                'slow_ma': current_slow,
                'cross_signal': current_cross
            },
            metadata={
                'feature_type': 'trend',
                'indicator_family': 'ma_cross',
                'lookback': cross_res.lookback,
                'warmup': cross_res.warmup_period,
                'lag': 'medium',
                'complexity': cross_res.metadata.get("complexity", "O(n)"),
                'memory_class': 'O(period)',
                'deterministic': True,
                'numeric_stability': 'high'
            },
            lineage={'dependencies': ['ftr-ohlcv']}
        )
