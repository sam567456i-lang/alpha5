import pandas as pd
import uuid
from typing import List, Any
from datetime import datetime

from Backend.price_geometry.contracts import AbstractGeometryEngine
from Backend.price_geometry.objects import Liquidity, Swing, LifecycleState, GeometryObject

class LiquidityEngine(AbstractGeometryEngine):
    """
    Detects liquidity pools (EQH/EQL, BSL/SSL) and manages deterministic decay policies.
    """
    def __init__(self, tolerance_pct: float = 0.001):
        # 0.1% tolerance for "equal" highs/lows
        self.tolerance_pct = tolerance_pct
        
    @property
    def engine_name(self) -> str:
        return "LiquidityEngine"
        
    @property
    def version(self) -> str:
        return "v1.0.0"

    def get_dependencies(self) -> List[str]:
        return ["SwingEngine"]

    def process(self, data: pd.DataFrame, context: Any = None) -> List[GeometryObject]:
        swings: List[Swing] = getattr(context, 'swings', [])
        dataset_id = getattr(context, 'dataset_id', "unknown_dataset")
        timeframe = getattr(context, 'timeframe', "unknown_tf")
        symbol = getattr(context, 'symbol', 'unknown')
        
        pools: List[Liquidity] = getattr(context, 'existing_pools', [])
        pool_dict = {p.id: p for p in pools}
        
        highs = [s for s in swings if s.is_high]
        lows = [s for s in swings if not s.is_high]
        
        outputs: List[GeometryObject] = []
        
        # O(N^2) naive scan for EQH/EQL. Can be optimized.
        # Find EQH
        for i in range(len(highs)):
            for j in range(i + 1, len(highs)):
                h1, h2 = highs[i], highs[j]
                if abs(h1.price - h2.price) / h1.price <= self.tolerance_pct:
                    new_pool = Liquidity(
                        id=f"EQH-{uuid.uuid4().hex[:8]}",
                        version=self.version,
                        dataset_id=dataset_id,
                        symbol=symbol,
                        timeframe=timeframe,
                        timestamp=h2.timestamp,
                        price=max(h1.price, h2.price),
                        parent_ids=[h1.id, h2.id],
                        generator=self.engine_name,
                        pool_type="EQH",
                        decay_policy="MITIGATION_OR_BREAK",
                        lifecycle_state=LifecycleState.CONFIRMED
                    )
                    pool_dict[new_pool.id] = new_pool
                    outputs.append(new_pool)
                    
        # Find EQL
        for i in range(len(lows)):
            for j in range(i + 1, len(lows)):
                l1, l2 = lows[i], lows[j]
                if abs(l1.price - l2.price) / l1.price <= self.tolerance_pct:
                    new_pool = Liquidity(
                        id=f"EQL-{uuid.uuid4().hex[:8]}",
                        version=self.version,
                        dataset_id=dataset_id,
                        symbol=symbol,
                        timeframe=timeframe,
                        timestamp=l2.timestamp, 
                        price=min(l1.price, l2.price),
                        parent_ids=[l1.id, l2.id],
                        generator=self.engine_name,
                        pool_type="EQL",
                        decay_policy="MITIGATION_OR_BREAK",
                        lifecycle_state=LifecycleState.CONFIRMED
                    )
                    pool_dict[new_pool.id] = new_pool
                    outputs.append(new_pool)

        # Decay Engine
        for i, row in data.iterrows():
            ts = i
            c_high = row['high']
            c_low = row['low']
            
            active_pools = [p for p in pool_dict.values() if p.lifecycle_state == LifecycleState.CONFIRMED and p.timestamp < ts]
            
            for pool in active_pools:
                # Mitigation/Sweep Policy
                if pool.pool_type in ("EQH", "BSL"):
                    if c_high > pool.price: # Swept
                        new_pool = pool.evolve(lifecycle_state=LifecycleState.INVALIDATED)
                        pool_dict[pool.id] = new_pool
                        outputs.append(new_pool)
                elif pool.pool_type in ("EQL", "SSL"):
                    if c_low < pool.price: # Swept
                        new_pool = pool.evolve(lifecycle_state=LifecycleState.INVALIDATED)
                        pool_dict[pool.id] = new_pool
                        outputs.append(new_pool)
        
        return outputs
