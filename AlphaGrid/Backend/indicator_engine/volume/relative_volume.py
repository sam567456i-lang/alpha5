import numpy as np
from Backend.indicator_engine.results import RelativeVolumeResult
from Backend.math.public.sma import calculate_sma
from Backend.market_data.market_series import MarketSeries

class RelativeVolumeEngine:
    """
    Relative Volume Engine.
    Computes Current Volume / SMA(Volume, period).
    """
    @staticmethod
    def compute(series: MarketSeries, period: int = 5) -> RelativeVolumeResult:
        if period <= 0:
            raise ValueError("Period must be > 0")
            
        sma_res = calculate_sma(
            values=series.volumes,
            timestamps=series.timestamps,
            period=period,
            input_column="volume"
        )
        
        # Calculate ratio
        with np.errstate(invalid='ignore', divide='ignore'):
            relative_vol = series.volumes / sma_res.values
            
        # If mean vol is 0, old logic returned 1.0
        relative_vol = np.where(sma_res.values == 0, 1.0, relative_vol)
        
        # Follow sma's valid mask
        valid_mask = sma_res.valid_mask
        relative_vol[~valid_mask] = np.nan
        
        return RelativeVolumeResult(
            timestamps=series.timestamps,
            valid_mask=valid_mask,
            warmup_period=sma_res.warmup_period,
            lookback=sma_res.lookback,
            metadata={"period": period},
            relative_volume=relative_vol
        )
