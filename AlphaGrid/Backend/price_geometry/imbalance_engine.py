import pandas as pd
import uuid
from typing import List, Any
from datetime import datetime

from Backend.price_geometry.contracts import AbstractGeometryEngine
from Backend.price_geometry.objects import Imbalance, LifecycleState, GeometryObject

class ImbalanceEngine(AbstractGeometryEngine):
    """
    Detects price imbalances (FVG, Inverse FVG, Volume Imbalances).
    """
    @property
    def engine_name(self) -> str:
        return "ImbalanceEngine"
        
    @property
    def version(self) -> str:
        return "v1.0.0"
        
    def get_dependencies(self) -> List[str]:
        return []

    def process(self, data: pd.DataFrame, context: Any = None) -> List[GeometryObject]:
        dataset_id = getattr(context, 'dataset_id', "unknown_dataset")
        timeframe = getattr(context, 'timeframe', "unknown_tf")
        symbol = getattr(context, 'symbol', 'unknown')
        
        # Pull existing imbalances from context if available
        imbalances: List[Imbalance] = getattr(context, 'existing_imbalances', [])
        imbalance_dict = {imb.id: imb for imb in imbalances}
        
        high = data['high'].values
        low = data['low'].values
        timestamps = data.index.to_pydatetime()
        
        outputs: List[GeometryObject] = []
        n = len(data)
        
        # O(N) scan for 3-bar FVGs
        for i in range(2, n):
            ts = timestamps[i]
            
            # Bullish FVG (Gap between Bar 1 High and Bar 3 Low)
            b1_h = high[i-2]
            b3_l = low[i]
            
            if b3_l > b1_h:
                new_imb = Imbalance(
                    id=f"FVG-BULL-{uuid.uuid4().hex[:8]}",
                    version=self.version,
                    dataset_id=dataset_id,
                    symbol=symbol,
                    timeframe=timeframe,
                    timestamp=ts,
                    price=(b3_l + b1_h) / 2.0, # Midpoint
                    generator=self.engine_name,
                    imbalance_type="FVG",
                    is_bullish=True,
                    top_price=b3_l,
                    bottom_price=b1_h,
                    size=b3_l - b1_h,
                    filled_pct=0.0,
                    lifecycle_state=LifecycleState.CONFIRMED
                )
                imbalance_dict[new_imb.id] = new_imb
                outputs.append(new_imb)
                
            # Bearish FVG (Gap between Bar 1 Low and Bar 3 High)
            b1_l = low[i-2]
            b3_h = high[i]
            
            if b3_h < b1_l:
                new_imb = Imbalance(
                    id=f"FVG-BEAR-{uuid.uuid4().hex[:8]}",
                    version=self.version,
                    dataset_id=dataset_id,
                    symbol=symbol,
                    timeframe=timeframe,
                    timestamp=ts,
                    price=(b3_h + b1_l) / 2.0, # Midpoint
                    generator=self.engine_name,
                    imbalance_type="FVG",
                    is_bullish=False,
                    top_price=b1_l,
                    bottom_price=b3_h,
                    size=b1_l - b3_h,
                    filled_pct=0.0,
                    lifecycle_state=LifecycleState.CONFIRMED
                )
                imbalance_dict[new_imb.id] = new_imb
                outputs.append(new_imb)
                
        # Mitigation / Fill Logic
        for i in range(n):
            ts = timestamps[i]
            c_high = high[i]
            c_low = low[i]
            
            active_imbs = [imb for imb in imbalance_dict.values() if imb.lifecycle_state == LifecycleState.CONFIRMED and imb.timestamp < ts]
            for imb in active_imbs:
                if imb.is_bullish:
                    # Filled if price trades below bottom_price
                    if c_low <= imb.bottom_price:
                        new_imb = imb.evolve(mitigated_price=c_low, filled_pct=1.0, lifecycle_state=LifecycleState.INVALIDATED)
                        imbalance_dict[imb.id] = new_imb
                        outputs.append(new_imb)
                    elif c_low < imb.top_price:
                        # Partial fill
                        filled = (imb.top_price - c_low) / imb.size if imb.size > 0 else 1.0
                        if filled > imb.filled_pct:
                            new_imb = imb.evolve(filled_pct=filled)
                            imbalance_dict[imb.id] = new_imb
                            outputs.append(new_imb)
                else:
                    # Filled if price trades above top_price
                    if c_high >= imb.top_price:
                        new_imb = imb.evolve(mitigated_price=c_high, filled_pct=1.0, lifecycle_state=LifecycleState.INVALIDATED)
                        imbalance_dict[imb.id] = new_imb
                        outputs.append(new_imb)
                    elif c_high > imb.bottom_price:
                        # Partial fill
                        filled = (c_high - imb.bottom_price) / imb.size if imb.size > 0 else 1.0
                        if filled > imb.filled_pct:
                            new_imb = imb.evolve(filled_pct=filled)
                            imbalance_dict[imb.id] = new_imb
                            outputs.append(new_imb)
        
        return outputs
