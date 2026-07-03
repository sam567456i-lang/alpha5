import pandas as pd
import uuid
from typing import List, Any
from datetime import datetime

from Backend.price_geometry.contracts import AbstractGeometryEngine
from Backend.price_geometry.objects import Range, LifecycleState

class RangeEngine(AbstractGeometryEngine):
    """
    Detects horizontal consolidation ranges from recent swings.
    """
    def __init__(self):
        self._name = "RangeEngine"
        
    @property
    def engine_name(self) -> str:
        return "RangeEngine"
        
    @property
    def version(self) -> str:
        return "v1.0.0"

    def process(self, data: pd.DataFrame, context: Any = None) -> List[Range]:
        dataset_id = getattr(context, 'dataset_id', "unknown_dataset")
        timeframe = getattr(context, 'timeframe', "unknown_tf")
        symbol = getattr(context, 'symbol', "unknown_symbol")
        cache = getattr(context, 'geometry_cache', None)
        
        if not cache:
            return []
            
        swings = cache.get_by_type("Swing", symbol)
        if len(swings) < 4:
            return []
            
        # Very simple heuristic: if the last 4 swings are contained within a tight price band
        last_4 = swings[-4:]
        highs = [s.price for s in last_4 if s.is_high]
        lows = [s.price for s in last_4 if not s.is_high]
        
        ranges: List[Range] = []
        
        if len(highs) >= 2 and len(lows) >= 2:
            max_high = max(highs)
            min_high = min(highs)
            max_low = max(lows)
            min_low = min(lows)
            
            # Check if highs are roughly equal and lows are roughly equal
            range_height = max_high - min_low
            if range_height > 0:
                if (max_high - min_high) / range_height < 0.2 and (max_low - min_low) / range_height < 0.2:
                    ranges.append(Range(
                        id=f"RANGE-{uuid.uuid4().hex[:8]}",
                        version=self.version,
                        dataset_id=dataset_id,
                        symbol=symbol,
                        timeframe=timeframe,
                        timestamp=last_4[-1].timestamp,
                        price=(max_high + min_low) / 2.0,
                        source_bars=[],
                        parent_ids=[s.id for s in last_4],
                        top_price=max_high,
                        bottom_price=min_low,
                        start_timestamp=last_4[0].timestamp,
                        end_timestamp=None,
                        is_broken=False,
                        lifecycle_state=LifecycleState.DETECTED
                    ))
                    
        return ranges
