from __future__ import annotations
from typing import TYPE_CHECKING
import numpy as np
if TYPE_CHECKING:
    import pandas as pd
import hashlib
import uuid
from typing import Dict, Any, Optional
from Backend.dtos.features import FeatureDTO
from Backend.features.interfaces.momentum_feature import MomentumFeatureInterface
from Backend.indicator_engine.runner import IndicatorRunner
from Backend.market_data.market_series import MarketSeries

class ROCFeatureGenerator(MomentumFeatureInterface):
    """
    Canonical Production Rate of Change (ROC) Generator.
    Delegates numerical composition strictly to the Indicator Engine.
    Strips semantic inference (momentum_strength, etc.) to the Concepts layer.
    """
    def __init__(self, period: int = 14):
        self.period = period
        self._component_id = f"ftr-roc-{period}"
        
    @property
    def component_id(self) -> str:
        return self._component_id
        
    def generate(self, data: pd.DataFrame, trace_id: str, correlation_id: str) -> FeatureDTO:
        if len(data) < self.period + 1:
            raise ValueError(f"Insufficient data. Required: {self.period + 1}")
            
        # Adapt pandas dataframe to Market Data Contract
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
        
        # Execute via IndicatorRunner
        roc_res = IndicatorRunner.execute(
            indicator_id="roc",
            series=series,
            period=self.period
        )
        
        if not roc_res.valid_mask[-1]:
            current_roc = float('nan')
        else:
            current_roc = float(roc_res.roc[-1])
            
        # Serialize safely handling NaN
        safe_roc = "NaN" if np.isnan(current_roc) else f"{current_roc}"
        payload_hash = hashlib.md5(safe_roc.encode()).hexdigest()
        
        return FeatureDTO(
            id=f"{self.component_id}-{uuid.uuid4().hex[:8]}",
            schema_version="1.0.0",
            producer=self.component_id,
            trace_id=trace_id,
            correlation_id=correlation_id,
            fingerprint=f"roc-{self.period}",
            checksum=payload_hash,
            symbol=series.symbol,
            timeframe=series.timeframe,
            values={
                'roc': current_roc
            },
            metadata={
                'feature_type': 'momentum',
                'indicator_family': 'roc',
                'lookback': roc_res.lookback,
                'warmup': roc_res.warmup_period,
                'lag': 'low',
                'complexity': roc_res.metadata.get("complexity", "O(n)"),
                'memory_class': 'O(period)',
                'deterministic': True,
                'numeric_stability': 'medium'
            },
            lineage={'dependencies': ['ftr-ohlcv']}
        )
