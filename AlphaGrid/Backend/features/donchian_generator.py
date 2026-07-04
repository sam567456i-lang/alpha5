from __future__ import annotations
from typing import TYPE_CHECKING
import numpy as np
if TYPE_CHECKING:
    import pandas as pd
import hashlib
import uuid
from typing import Dict, Any, Optional
from Backend.dtos.features import FeatureDTO
from Backend.features.interfaces.extremum_feature import ExtremumFeatureInterface
from Backend.indicator_engine.runner import IndicatorRunner
from Backend.market_data.market_series import MarketSeries

class DonchianFeatureGenerator(ExtremumFeatureInterface):
    """
    Canonical Production Donchian Channel Generator.
    Delegates numerical composition strictly to the Indicator Engine.
    """
    def __init__(self, period: int = 20):
        self.period = period
        self._component_id = f"ftr-donchian-{period}"
        
    @property
    def component_id(self) -> str:
        return self._component_id
        
    def generate(self, data: pd.DataFrame, trace_id: str, correlation_id: str) -> FeatureDTO:
        if len(data) < self.period:
            raise ValueError(f"Insufficient data. Required: {self.period}")
            
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
        
        result = IndicatorRunner.execute(
            indicator_id="donchian",
            series=series,
            period=self.period
        )
        
        if not result.valid_mask[-1]:
            cur_upper = float('nan')
            cur_lower = float('nan')
            cur_middle = float('nan')
            cur_bandwidth = float('nan')
        else:
            cur_upper = float(result.upper[-1])
            cur_lower = float(result.lower[-1])
            cur_middle = float(result.middle[-1])
            cur_bandwidth = float(result.bandwidth[-1])
        
        safe_payload = f"{'NaN' if np.isnan(cur_upper) else cur_upper}_{'NaN' if np.isnan(cur_lower) else cur_lower}"
        payload_hash = hashlib.md5(safe_payload.encode()).hexdigest()
        
        return FeatureDTO(
            id=f"{self.component_id}-{uuid.uuid4().hex[:8]}",
            schema_version="1.0.0",
            producer=self.component_id,
            trace_id=trace_id,
            correlation_id=correlation_id,
            fingerprint=f"donchian-{self.period}",
            checksum=payload_hash,
            symbol=series.symbol,
            timeframe=series.timeframe,
            values={
                'upper': cur_upper,
                'lower': cur_lower,
                'middle': cur_middle,
                'bandwidth': cur_bandwidth
            },
            metadata={
                'feature_type': 'extremum',
                'indicator_family': 'donchian',
                'lookback': result.lookback,
                'warmup': result.warmup_period,
                'lag': 'high',
                'complexity': 'O(N)',
                'memory_class': 'O(period)',
                'deterministic': True,
                'numeric_stability': 'high'
            },
            lineage={'dependencies': ['ftr-ohlcv']}
        )
