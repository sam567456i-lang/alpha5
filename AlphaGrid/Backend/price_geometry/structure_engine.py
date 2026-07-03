import pandas as pd
import uuid
from typing import List, Any
from datetime import datetime

from Backend.price_geometry.contracts import AbstractGeometryEngine
from Backend.price_geometry.objects import Structure, Swing, LifecycleState, GeometryObject

class StructureEngine(AbstractGeometryEngine):
    """
    Translates Swing objects into Market Structure (BOS, CHOCH).
    """
    @property
    def engine_name(self) -> str:
        return "StructureEngine"
        
    @property
    def version(self) -> str:
        return "v1.0.0"

    def get_dependencies(self) -> List[str]:
        return ["SwingEngine"]

    def process(self, data: pd.DataFrame, context: Any = None) -> List[GeometryObject]:
        """
        data: OHLCV DataFrame
        context: Must contain 'swings': List[Swing] and 'dataset_id', 'timeframe'
        """
        swings: List[Swing] = getattr(context, 'swings', [])
        dataset_id = getattr(context, 'dataset_id', "unknown_dataset")
        timeframe = getattr(context, 'timeframe', "unknown_tf")
        symbol = getattr(context, 'symbol', 'unknown')
        
        if not swings:
            return []
            
        swings = sorted(swings, key=lambda s: s.timestamp)
        outputs: List[GeometryObject] = []
        last_high: Swing = None
        last_low: Swing = None
        current_trend = 0 
        
        swing_dict = {s.id: s for s in swings}
        
        swing_idx = 0
        num_swings = len(swings)
        
        for row in data.itertuples():
            ts = row.Index
            c_price = row.close
            
            while swing_idx < num_swings and swings[swing_idx].timestamp <= ts:
                s = swings[swing_idx]
                if s.is_high:
                    last_high = s
                else:
                    last_low = s
                swing_dict[s.id] = s
                swing_idx += 1
                
            if not last_high or not last_low:
                continue
                
            if current_trend == 0:
                if c_price > last_high.price:
                    current_trend = 1
                elif c_price < last_low.price:
                    current_trend = -1
                continue
                
            if current_trend == 1:
                if c_price > last_high.price and last_high.lifecycle_state != LifecycleState.BROKEN:
                    outputs.append(Structure(
                        id=f"BOS-BULL-{uuid.uuid4().hex[:8]}",
                        version=self.version,
                        dataset_id=dataset_id,
                        symbol=symbol,
                        timeframe=timeframe,
                        timestamp=ts,
                        price=c_price,
                        parent_ids=[last_high.id],
                        structure_type="BOS",
                        is_bullish=True,
                        is_internal=False,
                        generator=self.engine_name,
                        lifecycle_state=LifecycleState.CONFIRMED
                    ))
                    last_high = last_high.evolve(lifecycle_state=LifecycleState.BROKEN)
                    swing_dict[last_high.id] = last_high
                    outputs.append(last_high)
                    
                elif c_price < last_low.price and last_low.lifecycle_state != LifecycleState.BROKEN:
                    outputs.append(Structure(
                        id=f"CHOCH-BEAR-{uuid.uuid4().hex[:8]}",
                        version=self.version,
                        dataset_id=dataset_id,
                        symbol=symbol,
                        timeframe=timeframe,
                        timestamp=ts,
                        price=c_price,
                        parent_ids=[last_low.id],
                        structure_type="CHOCH",
                        is_bullish=False,
                        is_internal=False,
                        generator=self.engine_name,
                        lifecycle_state=LifecycleState.CONFIRMED
                    ))
                    last_low = last_low.evolve(lifecycle_state=LifecycleState.BROKEN)
                    swing_dict[last_low.id] = last_low
                    outputs.append(last_low)
                    current_trend = -1
                    
            elif current_trend == -1:
                if c_price < last_low.price and last_low.lifecycle_state != LifecycleState.BROKEN:
                    outputs.append(Structure(
                        id=f"BOS-BEAR-{uuid.uuid4().hex[:8]}",
                        version=self.version,
                        dataset_id=dataset_id,
                        symbol=symbol,
                        timeframe=timeframe,
                        timestamp=ts,
                        price=c_price,
                        parent_ids=[last_low.id],
                        structure_type="BOS",
                        is_bullish=False,
                        is_internal=False,
                        generator=self.engine_name,
                        lifecycle_state=LifecycleState.CONFIRMED
                    ))
                    last_low = last_low.evolve(lifecycle_state=LifecycleState.BROKEN)
                    swing_dict[last_low.id] = last_low
                    outputs.append(last_low)
                    
                elif c_price > last_high.price and last_high.lifecycle_state != LifecycleState.BROKEN:
                    outputs.append(Structure(
                        id=f"CHOCH-BULL-{uuid.uuid4().hex[:8]}",
                        version=self.version,
                        dataset_id=dataset_id,
                        symbol=symbol,
                        timeframe=timeframe,
                        timestamp=ts,
                        price=c_price,
                        parent_ids=[last_high.id],
                        structure_type="CHOCH",
                        is_bullish=True,
                        is_internal=False,
                        generator=self.engine_name,
                        lifecycle_state=LifecycleState.CONFIRMED
                    ))
                    last_high = last_high.evolve(lifecycle_state=LifecycleState.BROKEN)
                    swing_dict[last_high.id] = last_high
                    outputs.append(last_high)
                    current_trend = 1
                    
        return outputs
