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

class MACDFeatureGenerator(MomentumFeatureInterface):
    """
    Canonical Production MACD Generator.
    Delegates numerical composition strictly to the Indicator Engine.
    Strips semantic inference (momentum_strength, etc.) to the Concepts layer.
    """
    def __init__(self, fast_period: int = 12, slow_period: int = 26, signal_period: int = 9):
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.signal_period = signal_period
        self._component_id = f"ftr-macd-{fast_period}-{slow_period}-{signal_period}"
        
    @property
    def component_id(self) -> str:
        return self._component_id
        
    def generate(self, data: pd.DataFrame, trace_id: str, correlation_id: str) -> FeatureDTO:
        if len(data) < self.slow_period + self.signal_period:
            raise ValueError(f"Insufficient data. Required: {self.slow_period + self.signal_period}")
            
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
        macd_res = IndicatorRunner.execute(
            indicator_id="macd",
            series=series,
            fast_period=self.fast_period,
            slow_period=self.slow_period,
            signal_period=self.signal_period
        )
        
        if not macd_res.valid_mask[-1]:
            current_macd = float('nan')
            current_signal = float('nan')
            current_hist = float('nan')
        else:
            current_macd = float(macd_res.macd[-1])
            current_signal = float(macd_res.signal[-1])
            current_hist = float(macd_res.histogram[-1])
        
        # Serialize safely handling NaN
        safe_payload = f"{'NaN' if np.isnan(current_macd) else current_macd}_{'NaN' if np.isnan(current_signal) else current_signal}_{'NaN' if np.isnan(current_hist) else current_hist}"
        payload_hash = hashlib.md5(safe_payload.encode()).hexdigest()
        
        return FeatureDTO(
            id=f"{self.component_id}-{uuid.uuid4().hex[:8]}",
            schema_version="1.0.0",
            producer=self.component_id,
            trace_id=trace_id,
            correlation_id=correlation_id,
            fingerprint=f"macd-{self.fast_period}-{self.slow_period}-{self.signal_period}",
            checksum=payload_hash,
            symbol=series.symbol,
            timeframe=series.timeframe,
            values={
                'macd_line': current_macd,
                'signal_line': current_signal,
                'histogram': current_hist
            },
            metadata={
                'feature_type': 'momentum',
                'indicator_family': 'macd',
                'lookback': macd_res.lookback,
                'warmup': macd_res.warmup_period,
                'lag': 'medium',
                'complexity': macd_res.metadata.get("complexity", "O(n)"),
                'memory_class': 'O(period)',
                'deterministic': True,
                'numeric_stability': 'high'
            },
            lineage={'dependencies': ['ftr-ohlcv']}
        )
