import pandas as pd
import numpy as np
import uuid
from typing import List, Any
from datetime import datetime

from Backend.price_geometry.contracts import AbstractGeometryEngine
from Backend.price_geometry.objects import Pivot, LifecycleState

class PivotEngine(AbstractGeometryEngine):
    """
    Detects market pivots (Highs and Lows) using static or adaptive fractal strength.
    A Pivot is purely mathematical (e.g., highest high of N bars left and right).
    """
    def __init__(self, mode: str = "adaptive", default_strength: int = 5):
        """
        mode: 'static' or 'adaptive'.
        default_strength: Used in static mode. In adaptive mode, serves as a baseline.
        """
        self.mode = mode
        self.default_strength = default_strength
        self._name = "PivotEngine"
        
    @property
    def engine_name(self) -> str:
        return "PivotEngine"
        
    @property
    def version(self) -> str:
        return "v1.0.0"

    def _calculate_atr(self, data: pd.DataFrame, period: int = 14) -> pd.Series:
        high = data['high']
        low = data['low']
        close_prev = data['close'].shift(1)
        
        tr1 = high - low
        tr2 = (high - close_prev).abs()
        tr3 = (low - close_prev).abs()
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        return tr.rolling(window=period).mean()

    def process(self, data: pd.DataFrame, context: Any = None) -> List[Pivot]:
        """
        Process OHLCV dataframe and return list of immutable Pivot objects.
        """
        dataset_id = getattr(context, 'dataset_id', "unknown_dataset")
        timeframe = getattr(context, 'timeframe', "unknown_tf")
        symbol = getattr(context, 'symbol', "unknown_symbol")
        
        pivots: List[Pivot] = []
        
        if self.mode == "adaptive":
            atr = self._calculate_atr(data)
            atr_pct = atr / data['close']
            median_atr = atr_pct.median()
            if pd.isna(median_atr): median_atr = 0.001
        
        close = data['close'].values
        high = data['high'].values
        low = data['low'].values
        timestamps = data.index.to_pydatetime()
        
        n = len(data)
        for i in range(n):
            if self.mode == "adaptive":
                curr_atr_pct = (high[i] - low[i]) / close[i] if close[i] != 0 else 0
                if curr_atr_pct > median_atr * 1.5:
                    strength = 3
                elif curr_atr_pct < median_atr * 0.5:
                    strength = 7
                else:
                    strength = 5
            else:
                strength = self.default_strength
                
            if i - strength < 0 or i + strength >= n:
                continue
                
            is_high = True
            for j in range(1, strength + 1):
                if high[i - j] >= high[i] or high[i + j] > high[i]:
                    is_high = False
                    break
                    
            if is_high:
                pivots.append(Pivot(
                    id=f"PIVOT-H-{uuid.uuid4().hex[:8]}",
                    version=self.version,
                    dataset_id=dataset_id,
                    symbol=symbol,
                    timeframe=timeframe,
                    timestamp=timestamps[i],
                    price=float(high[i]),
                    source_bars=[timestamps[i].isoformat()],
                    is_high=True,
                    left_bars=strength,
                    right_bars=strength,
                    lifecycle_state=LifecycleState.CONFIRMED
                ))
                
            is_low = True
            for j in range(1, strength + 1):
                if low[i - j] <= low[i] or low[i + j] < low[i]:
                    is_low = False
                    break
                    
            if is_low:
                pivots.append(Pivot(
                    id=f"PIVOT-L-{uuid.uuid4().hex[:8]}",
                    version=self.version,
                    dataset_id=dataset_id,
                    symbol=symbol,
                    timeframe=timeframe,
                    timestamp=timestamps[i],
                    price=float(low[i]),
                    source_bars=[timestamps[i].isoformat()],
                    is_high=False,
                    left_bars=strength,
                    right_bars=strength,
                    lifecycle_state=LifecycleState.CONFIRMED
                ))
                
        return pivots
