import pandas as pd
import numpy as np
import uuid
from typing import List, Any, Dict
from datetime import datetime

from Backend.price_geometry.contracts import AbstractGeometryEngine
from Backend.price_geometry.objects import Swing, LifecycleState

class SwingEngine(AbstractGeometryEngine):
    """
    Detects market swings (Highs and Lows) using static or adaptive fractal strength.
    """
    def __init__(self, mode: str = "adaptive", default_strength: int = 3):
        """
        mode: 'static' or 'adaptive'.
        default_strength: Used in static mode. In adaptive mode, serves as a baseline.
        """
        self.mode = mode
        self.default_strength = default_strength
        self._name = "SwingEngine"
        
    @property
    def engine_name(self) -> str:
        return "SwingEngine"
        
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

    def process(self, data: pd.DataFrame, context: Any = None) -> List[Swing]:
        """
        Process Pivot objects from the context cache and generate Swings.
        A Swing connects major pivots, filtering out internal/minor pivots.
        """
        dataset_id = getattr(context, 'dataset_id', "unknown_dataset")
        timeframe = getattr(context, 'timeframe', "unknown_tf")
        symbol = getattr(context, 'symbol', "unknown_symbol")
        cache = getattr(context, 'geometry_cache', None)
        
        if not cache:
            return []
            
        pivots = cache.get_by_type("Pivot", symbol)
        if not pivots:
            return []
            
        # Sort pivots chronologically
        pivots.sort(key=lambda p: p.timestamp)
        
        swings: List[Swing] = []
        
        # Simple algorithm: A Swing is a higher-timeframe or stronger pivot.
        # We filter pivots that have left/right bars >= self.default_strength
        # In a real institutional engine, this would build a Swing Tree.
        for p in pivots:
            if getattr(p, 'left_bars', 0) >= self.default_strength and getattr(p, 'right_bars', 0) >= self.default_strength:
                swing = Swing(
                    id=f"SWING-{'H' if p.is_high else 'L'}-{uuid.uuid4().hex[:8]}",
                    version=self.version,
                    dataset_id=dataset_id,
                    symbol=symbol,
                    timeframe=timeframe,
                    timestamp=p.timestamp,
                    price=p.price,
                    source_bars=[p.timestamp.isoformat()],
                    parent_ids=[p.id],
                    is_high=p.is_high,
                    strength=getattr(p, 'left_bars', self.default_strength),
                    is_internal=False,
                    lifecycle_state=LifecycleState.CONFIRMED
                )
                swings.append(swing)
                
        return swings
