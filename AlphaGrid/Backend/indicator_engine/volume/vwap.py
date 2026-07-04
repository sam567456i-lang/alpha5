import numpy as np
from Backend.indicator_engine.results import VWAPResult
from Backend.math.public.vwap import calculate_vwap
from Backend.market_data.market_series import MarketSeries

class VWAPEngine:
    """
    Volume Weighted Average Price (VWAP) Engine.
    """
    @staticmethod
    def compute(series: MarketSeries) -> VWAPResult:
        # VWAP typical price = (High + Low + Close) / 3
        typical_price = (series.highs + series.lows + series.closes) / 3.0
        
        res = calculate_vwap(
            typical_price=typical_price,
            volume=series.volumes,
            timestamps=series.timestamps,
            input_column="typical_price"
        )
        
        return VWAPResult(
            timestamps=series.timestamps,
            valid_mask=res.valid_mask,
            warmup_period=res.warmup_period,
            lookback=res.lookback,
            metadata={"period": "session"},
            vwap=res.values
        )
