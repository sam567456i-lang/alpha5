import pandas as pd
import uuid
from typing import List, Any
from datetime import datetime

from Backend.price_geometry.contracts import AbstractGeometryEngine
from Backend.price_geometry.objects import Channel, LifecycleState

class ChannelEngine(AbstractGeometryEngine):
    """
    Detects channels by analyzing parallel support and resistance trendlines.
    """
    def __init__(self):
        self._name = "ChannelEngine"
        
    @property
    def engine_name(self) -> str:
        return "ChannelEngine"
        
    @property
    def version(self) -> str:
        return "v1.0.0"

    def process(self, data: pd.DataFrame, context: Any = None) -> List[Channel]:
        dataset_id = getattr(context, 'dataset_id', "unknown_dataset")
        timeframe = getattr(context, 'timeframe', "unknown_tf")
        symbol = getattr(context, 'symbol', "unknown_symbol")
        cache = getattr(context, 'geometry_cache', None)
        
        if not cache:
            return []
            
        trendlines = cache.get_by_type("Trendline", symbol)
        if len(trendlines) < 2:
            return []
            
        supports = [tl for tl in trendlines if tl.is_support]
        resistances = [tl for tl in trendlines if not tl.is_support]
        
        channels: List[Channel] = []
        
        # Simple heuristic: pair the most recent support and resistance if slopes are similar
        if supports and resistances:
            sup = supports[-1]
            res = resistances[-1]
            
            # Check slope similarity (e.g. within 20%)
            if abs(sup.slope - res.slope) < max(abs(sup.slope), abs(res.slope)) * 0.2:
                width = abs(res.price - sup.price)
                is_asc = sup.slope > 0
                channels.append(Channel(
                    id=f"CHAN-{'ASC' if is_asc else 'DESC'}-{uuid.uuid4().hex[:8]}",
                    version=self.version,
                    dataset_id=dataset_id,
                    symbol=symbol,
                    timeframe=timeframe,
                    timestamp=max(sup.timestamp, res.timestamp),
                    price=(sup.price + res.price) / 2.0,
                    source_bars=[],
                    parent_ids=[sup.id, res.id],
                    upper_trendline_id=res.id,
                    lower_trendline_id=sup.id,
                    is_ascending=is_asc,
                    width=width,
                    lifecycle_state=LifecycleState.DETECTED
                ))
                
        return channels
