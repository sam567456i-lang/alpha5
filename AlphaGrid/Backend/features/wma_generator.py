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

class WMAFeatureGenerator(TrendFeatureInterface):
    """
    Canonical Production WMA Generator.
    Delegates numerical composition strictly to the Indicator Engine.
    """
    def __init__(self, period: int = 20):
        self.period = period
        self._component_id = f"ftr-wma-{period}"
        
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
        
        wma_res = IndicatorRunner.execute(
            indicator_id="wma",
            series=series,
            period=self.period
        )
        
        if not wma_res.valid_mask[-1]:
            current_wma = float('nan')
        else:
            current_wma = float(wma_res.wma[-1])
        
        safe_payload = f"{'NaN' if np.isnan(current_wma) else current_wma}"
        payload_hash = hashlib.md5(safe_payload.encode()).hexdigest()
        
        return FeatureDTO(
            id=f"{self.component_id}-{uuid.uuid4().hex[:8]}",
            schema_version="1.0.0",
            producer=self.component_id,
            trace_id=trace_id,
            correlation_id=correlation_id,
            fingerprint=f"wma-{self.period}",
            checksum=payload_hash,
            symbol=series.symbol,
            timeframe=series.timeframe,
            values={
                'wma': current_wma
            },
            metadata={
                'feature_type': 'trend',
                'indicator_family': 'wma',
                'lookback': wma_res.lookback,
                'warmup': wma_res.warmup_period,
                'lag': 'medium',
                'complexity': wma_res.metadata.get("complexity", "O(n)"),
                'memory_class': 'O(period)',
                'deterministic': True,
                'numeric_stability': 'high'
            },
            lineage={'dependencies': ['ftr-ohlcv']}
        )
