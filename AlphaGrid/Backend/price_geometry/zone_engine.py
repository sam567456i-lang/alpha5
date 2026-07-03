import pandas as pd
import uuid
from typing import List, Any

from Backend.price_geometry.contracts import AbstractGeometryEngine
from Backend.price_geometry.objects import Zone, Swing, LifecycleState

class ZoneEngine(AbstractGeometryEngine):
    """
    Computes unified structural zones: Premium, Discount, Equilibrium, Supply, and Demand.
    """
    @property
    def engine_name(self) -> str:
        return "ZoneEngine"
        
    @property
    def version(self) -> str:
        return "v1.0.0"

    def process(self, data: pd.DataFrame, context: Any = None) -> List[Zone]:
        swings: List[Swing] = getattr(context, 'swings', [])
        dataset_id = getattr(context, 'dataset_id', "unknown_dataset")
        timeframe = getattr(context, 'timeframe', "unknown_tf")
        
        zones: List[Zone] = []
        
        # Sort swings chronologically
        swings = sorted(swings, key=lambda s: s.timestamp)
        if len(swings) < 2:
            return []
            
        # Iterate over adjacent swings to define trading ranges (legs)
        for i in range(1, len(swings)):
            s1 = swings[i-1]
            s2 = swings[i]
            
            # Ensure they are opposite polarity (High -> Low or Low -> High)
            if s1.is_high == s2.is_high:
                continue
                
            high_price = max(s1.price, s2.price)
            low_price = min(s1.price, s2.price)
            midpoint = (high_price + low_price) / 2.0
            
            range_id = f"LEG-{s1.id[-8:]}-{s2.id[-8:]}"
            
            # Premium Zone (Top 50%)
            zones.append(Zone(
                id=f"PREM-{uuid.uuid4().hex[:8]}",
                version=self.version,
                dataset_id=dataset_id,
                timeframe=timeframe,
                timestamp=s2.timestamp,
                price=midpoint + (high_price - midpoint) / 2.0,
                parent_ids=[s1.id, s2.id],
                zone_type="PREMIUM",
                top_price=high_price,
                bottom_price=midpoint,
                lifecycle_state=LifecycleState.CONFIRMED
            ))
            
            # Discount Zone (Bottom 50%)
            zones.append(Zone(
                id=f"DISC-{uuid.uuid4().hex[:8]}",
                version=self.version,
                dataset_id=dataset_id,
                timeframe=timeframe,
                timestamp=s2.timestamp,
                price=midpoint - (midpoint - low_price) / 2.0,
                parent_ids=[s1.id, s2.id],
                zone_type="DISCOUNT",
                top_price=midpoint,
                bottom_price=low_price,
                lifecycle_state=LifecycleState.CONFIRMED
            ))
            
            # Equilibrium
            zones.append(Zone(
                id=f"EQ-{uuid.uuid4().hex[:8]}",
                version=self.version,
                dataset_id=dataset_id,
                timeframe=timeframe,
                timestamp=s2.timestamp,
                price=midpoint,
                parent_ids=[s1.id, s2.id],
                zone_type="EQUILIBRIUM",
                top_price=midpoint + (high_price - low_price) * 0.05,
                bottom_price=midpoint - (high_price - low_price) * 0.05,
                lifecycle_state=LifecycleState.CONFIRMED
            ))
            
        return zones
