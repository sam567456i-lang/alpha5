import pandas as pd
import uuid
from typing import List, Any
from datetime import datetime

from Backend.price_geometry.contracts import AbstractGeometryEngine
from Backend.price_geometry.objects import Trendline, LifecycleState

class TrendlineEngine(AbstractGeometryEngine):
    """
    Detects trendlines by connecting consecutive Swing Highs or Swing Lows.
    """
    def __init__(self, max_lookback_swings: int = 10, min_touches: int = 2):
        self.max_lookback = max_lookback_swings
        self.min_touches = min_touches
        self._name = "TrendlineEngine"
        
    @property
    def engine_name(self) -> str:
        return "TrendlineEngine"
        
    @property
    def version(self) -> str:
        return "v1.0.0"

    def process(self, data: pd.DataFrame, context: Any = None) -> List[Trendline]:
        dataset_id = getattr(context, 'dataset_id', "unknown_dataset")
        timeframe = getattr(context, 'timeframe', "unknown_tf")
        symbol = getattr(context, 'symbol', "unknown_symbol")
        cache = getattr(context, 'geometry_cache', None)
        
        if not cache:
            return []
            
        swings = cache.get_by_type("Swing", symbol)
        if len(swings) < 2:
            return []
            
        swings.sort(key=lambda s: s.timestamp)
        swing_highs = [s for s in swings if s.is_high][-self.max_lookback:]
        swing_lows = [s for s in swings if not s.is_high][-self.max_lookback:]
        
        trendlines: List[Trendline] = []
        
        # Very simple heuristic: connect the last two swing highs/lows
        if len(swing_highs) >= 2:
            s1 = swing_highs[-2]
            s2 = swing_highs[-1]
            if s2.price < s1.price: # Downward trendline
                dt = (s2.timestamp - s1.timestamp).total_seconds()
                dp = s2.price - s1.price
                slope = dp / dt if dt > 0 else 0
                trendlines.append(Trendline(
                    id=f"TL-RES-{uuid.uuid4().hex[:8]}",
                    version=self.version,
                    dataset_id=dataset_id,
                    symbol=symbol,
                    timeframe=timeframe,
                    timestamp=s2.timestamp,
                    price=s2.price,
                    source_bars=[s1.timestamp.isoformat(), s2.timestamp.isoformat()],
                    parent_ids=[s1.id, s2.id],
                    start_point_id=s1.id,
                    end_point_id=s2.id,
                    slope=slope,
                    is_support=False,
                    touches=2,
                    lifecycle_state=LifecycleState.DETECTED
                ))
                
        if len(swing_lows) >= 2:
            s1 = swing_lows[-2]
            s2 = swing_lows[-1]
            if s2.price > s1.price: # Upward trendline
                dt = (s2.timestamp - s1.timestamp).total_seconds()
                dp = s2.price - s1.price
                slope = dp / dt if dt > 0 else 0
                trendlines.append(Trendline(
                    id=f"TL-SUP-{uuid.uuid4().hex[:8]}",
                    version=self.version,
                    dataset_id=dataset_id,
                    symbol=symbol,
                    timeframe=timeframe,
                    timestamp=s2.timestamp,
                    price=s2.price,
                    source_bars=[s1.timestamp.isoformat(), s2.timestamp.isoformat()],
                    parent_ids=[s1.id, s2.id],
                    start_point_id=s1.id,
                    end_point_id=s2.id,
                    slope=slope,
                    is_support=True,
                    touches=2,
                    lifecycle_state=LifecycleState.DETECTED
                ))
                
        return trendlines
