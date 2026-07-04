from __future__ import annotations
from typing import TYPE_CHECKING
import numpy as np
if TYPE_CHECKING:
    import pandas as pd
import hashlib
import uuid
from typing import Dict, Any, Optional
from Backend.dtos.features import FeatureDTO
from Backend.features.interfaces.volatility_feature import VolatilityFeatureInterface
from Backend.indicator_engine.runner import IndicatorRunner
from Backend.market_data.market_series import MarketSeries

class KeltnerFeatureGenerator(VolatilityFeatureInterface):
    """
    Canonical Production Keltner Channels Generator.
    Delegates numerical composition strictly to the Indicator Engine.
    """
    def __init__(self, period: int = 20, atr_period: int = 10, multiplier: float = 2.0):
        self.period = period
        self.atr_period = atr_period
        self.multiplier = multiplier
        self._component_id = f"ftr-keltner-{period}-{atr_period}-{multiplier}"
        
    @property
    def component_id(self) -> str:
        return self._component_id
        
    def generate(self, data: pd.DataFrame, trace_id: str, correlation_id: str) -> FeatureDTO:
        req_len = max(self.period, self.atr_period)
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
        
        keltner_res = IndicatorRunner.execute(
            indicator_id="keltner",
            series=series,
            period=self.period,
            atr_period=self.atr_period,
            multiplier=self.multiplier
        )
        
        if not keltner_res.valid_mask[-1]:
            current_upper = float('nan')
            current_middle = float('nan')
            current_lower = float('nan')
        else:
            current_upper = float(keltner_res.upper[-1])
            current_middle = float(keltner_res.middle[-1])
            current_lower = float(keltner_res.lower[-1])
        
        safe_payload = f"{'NaN' if np.isnan(current_middle) else current_middle}"
        payload_hash = hashlib.md5(safe_payload.encode()).hexdigest()
        
        return FeatureDTO(
            id=f"{self.component_id}-{uuid.uuid4().hex[:8]}",
            schema_version="1.0.0",
            producer=self.component_id,
            trace_id=trace_id,
            correlation_id=correlation_id,
            fingerprint=f"keltner-{self.period}-{self.atr_period}-{self.multiplier}",
            checksum=payload_hash,
            symbol=series.symbol,
            timeframe=series.timeframe,
            values={
                'upper': current_upper,
                'middle': current_middle,
                'lower': current_lower
            },
            metadata={
                'feature_type': 'volatility',
                'indicator_family': 'keltner',
                'lookback': keltner_res.lookback,
                'warmup': keltner_res.warmup_period,
                'lag': 'medium',
                'complexity': keltner_res.metadata.get("complexity", "O(n)"),
                'memory_class': 'O(period)',
                'deterministic': True,
                'numeric_stability': 'high'
            },
            lineage={'dependencies': ['ftr-ohlcv']}
        )
