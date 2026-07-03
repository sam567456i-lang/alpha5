from typing import List, Any, Dict
import pandas as pd
import uuid
from datetime import datetime
from dataclasses import dataclass

from Backend.price_geometry.contracts import AbstractGeometryEngine
from Backend.price_geometry.objects import Structure, LifecycleState, GeometryObject

@dataclass(frozen=True)
class ConflictEvent(GeometryObject):
    conflict_type: str = "MTF_ALIGNMENT"
    is_aligned: bool = False
    bullish_timeframes: List[str] = None
    bearish_timeframes: List[str] = None

class ConflictEngine(AbstractGeometryEngine):
    """
    Evaluates multi-timeframe geometric alignment.
    Detects structural conflicts (e.g., Weekly Bullish + Daily Bullish + 15m Bearish = Conflict).
    Outputs deterministic Evidence for the Evidence Engine.
    """
    @property
    def engine_name(self) -> str:
        return "ConflictEngine"
        
    @property
    def version(self) -> str:
        return "v1.0.0"

    def process(self, data: pd.DataFrame, context: Any = None) -> List[ConflictEvent]:
        # Context should contain active structures grouped by timeframe
        mtf_structures: Dict[str, List[Structure]] = getattr(context, 'mtf_structures', {})
        dataset_id = getattr(context, 'dataset_id', "unknown_dataset")
        
        # Determine current trend per timeframe based on the latest confirmed structure
        trends = {}
        for tf, structures in mtf_structures.items():
            confirmed = [s for s in structures if s.lifecycle_state == LifecycleState.CONFIRMED]
            if confirmed:
                latest = sorted(confirmed, key=lambda x: x.timestamp)[-1]
                trends[tf] = latest.is_bullish
                
        if not trends:
            return []
            
        bullish_tfs = [tf for tf, is_bull in trends.items() if is_bull]
        bearish_tfs = [tf for tf, is_bull in trends.items() if not is_bull]
        
        is_aligned = len(bullish_tfs) == 0 or len(bearish_tfs) == 0
        
        ts = data.index[-1] if not data.empty else datetime.utcnow()
        price = data['close'].iloc[-1] if not data.empty else 0.0
        
        event = ConflictEvent(
            id=f"CONF-{uuid.uuid4().hex[:8]}",
            version=self.version,
            dataset_id=dataset_id,
            timeframe="MTF",
            timestamp=ts,
            price=price,
            parent_ids=[], # Can link to the latest structures forming the conflict
            conflict_type="MTF_ALIGNMENT",
            is_aligned=is_aligned,
            bullish_timeframes=bullish_tfs,
            bearish_timeframes=bearish_tfs,
            lifecycle_state=LifecycleState.CONFIRMED
        )
        
        return [event]
