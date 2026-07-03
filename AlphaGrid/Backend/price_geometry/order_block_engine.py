import pandas as pd
import uuid
from typing import List, Any
from datetime import datetime

from Backend.price_geometry.contracts import AbstractGeometryEngine
from Backend.price_geometry.objects import OrderBlock, Structure, Swing, LifecycleState, GeometryObject

class OrderBlockEngine(AbstractGeometryEngine):
    """
    Detects Order Blocks by analyzing structural breaks (BOS/CHOCH) and tracing back to the origin swing.
    """
    @property
    def engine_name(self) -> str:
        return "OrderBlockEngine"
        
    @property
    def version(self) -> str:
        return "v1.0.0"

    def get_dependencies(self) -> List[str]:
        return ["SwingEngine", "StructureEngine"]

    def process(self, data: pd.DataFrame, context: Any = None) -> List[GeometryObject]:
        structures: List[Structure] = getattr(context, 'structures', [])
        swings: List[Swing] = getattr(context, 'swings', [])
        dataset_id = getattr(context, 'dataset_id', "unknown_dataset")
        timeframe = getattr(context, 'timeframe', "unknown_tf")
        symbol = getattr(context, 'symbol', 'unknown')
        
        outputs: List[GeometryObject] = []
        
        # Pull existing OBs to evaluate mitigation
        existing_obs: List[OrderBlock] = getattr(context, 'existing_obs', [])
        ob_dict = {ob.id: ob for ob in existing_obs}
        
        swings_by_ts = {s.timestamp: s for s in swings}
        
        # High and low arrays for mitigation checks
        high = data['high'].values
        low = data['low'].values
        timestamps = data.index.to_pydatetime()
        
        # Pre-calculate to avoid O(N^2) search
        for struct in structures:
            # We only generate OBs on confirmed structure breaks
            if struct.lifecycle_state != LifecycleState.CONFIRMED:
                continue
                
            # A Structure break has parent_ids (the swing that was broken).
            # But the Order Block is at the origin of the impulse that broke it.
            # E.g. Bullish BOS -> Broken Swing High. We need the preceding Swing Low.
            broken_swing_id = struct.parent_ids[0] if struct.parent_ids else None
            broken_swing = next((s for s in swings if s.id == broken_swing_id), None)
            
            if not broken_swing:
                continue
                
            # Find the impulse origin swing (the swing immediately preceding the broken swing, or the absolute high/low before it)
            # Simplest approximation for the origin swing is the swing of opposite polarity immediately before the break.
            preceding_swings = [s for s in swings if s.timestamp < struct.timestamp]
            if not preceding_swings:
                continue
                
            if struct.is_bullish:
                # Bullish break (BOS or CHOCH) -> Look for the lowest Swing Low before the break
                origin_lows = [s for s in preceding_swings if not s.is_high]
                if not origin_lows:
                    continue
                origin_swing = origin_lows[-1]
                
                # Order block is typically the last down candle. For now, we estimate the OB zone using the swing's price.
                # In a full implementation, we'd scan `data` around origin_swing.timestamp for the specific candle.
                # Here we define the OB zone from the swing low to slightly above it.
                bottom = origin_swing.price
                # Approximate top by taking the high of the swing low candle
                if origin_swing.timestamp in data.index:
                    top = data.loc[origin_swing.timestamp]['high']
                else:
                    top = bottom * 1.002 # 0.2% buffer if exact candle not found
                    
                new_ob = OrderBlock(
                    id=f"OB-BULL-{uuid.uuid4().hex[:8]}",
                    version=self.version,
                    dataset_id=dataset_id,
                    symbol=symbol,
                    timeframe=timeframe,
                    timestamp=struct.timestamp, # OB is confirmed when the structure breaks
                    price=(top + bottom) / 2.0,
                    generator=self.engine_name,
                    parent_ids=[struct.id, origin_swing.id],
                    ob_type="OB",
                    is_bullish=True,
                    top_price=top,
                    bottom_price=bottom,
                    lifecycle_state=LifecycleState.CONFIRMED
                )
                ob_dict[new_ob.id] = new_ob
                outputs.append(new_ob)
                
            else:
                # Bearish break -> Look for highest Swing High before the break
                origin_highs = [s for s in preceding_swings if s.is_high]
                if not origin_highs:
                    continue
                origin_swing = origin_highs[-1]
                
                top = origin_swing.price
                if origin_swing.timestamp in data.index:
                    bottom = data.loc[origin_swing.timestamp]['low']
                else:
                    bottom = top * 0.998
                    
                new_ob = OrderBlock(
                    id=f"OB-BEAR-{uuid.uuid4().hex[:8]}",
                    version=self.version,
                    dataset_id=dataset_id,
                    symbol=symbol,
                    timeframe=timeframe,
                    timestamp=struct.timestamp,
                    price=(top + bottom) / 2.0,
                    generator=self.engine_name,
                    parent_ids=[struct.id, origin_swing.id],
                    ob_type="OB",
                    is_bullish=False,
                    top_price=top,
                    bottom_price=bottom,
                    lifecycle_state=LifecycleState.CONFIRMED
                )
                ob_dict[new_ob.id] = new_ob
                outputs.append(new_ob)

        # Mitigation Engine for Order Blocks
        for i in range(len(data)):
            ts = timestamps[i]
            c_high = high[i]
            c_low = low[i]
            c_close = data['close'].iloc[i]
            
            active_obs = [ob for ob in ob_dict.values() if ob.lifecycle_state == LifecycleState.CONFIRMED and ob.timestamp < ts]
            for ob in active_obs:
                if ob.is_bullish:
                    # Broken if it closes below the bottom of the OB
                    if c_close < ob.bottom_price:
                        new_ob = ob.evolve(lifecycle_state=LifecycleState.BROKEN)
                        ob_dict[ob.id] = new_ob
                        outputs.append(new_ob)
                    # Mitigated if price touches the OB zone
                    elif c_low <= ob.top_price:
                        new_ob = ob.evolve(lifecycle_state=LifecycleState.MITIGATED, mitigated_price=c_low)
                        ob_dict[ob.id] = new_ob
                        outputs.append(new_ob)
                else:
                    # Broken if it closes above the top of the OB
                    if c_close > ob.top_price:
                        new_ob = ob.evolve(lifecycle_state=LifecycleState.BROKEN)
                        ob_dict[ob.id] = new_ob
                        outputs.append(new_ob)
                    # Mitigated if price touches the OB zone
                    elif c_high >= ob.bottom_price:
                        new_ob = ob.evolve(lifecycle_state=LifecycleState.MITIGATED, mitigated_price=c_high)
                        ob_dict[ob.id] = new_ob
                        outputs.append(new_ob)
                        
        return outputs
