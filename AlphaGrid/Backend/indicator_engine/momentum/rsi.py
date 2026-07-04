import numpy as np
from Backend.indicator_engine.results import RSIResult
from Backend.math.public.diff import calculate_diff
from Backend.math.public.rma import calculate_rma
from Backend.math.public.clip import calculate_clip

class RSIEngine:
    """
    Relative Strength Index Engine.
    Computes Wilder's RSI using the Math Core primitives.
    """
    @staticmethod
    def compute(close: np.ndarray, timestamps: np.ndarray, period: int = 14) -> RSIResult:
        if period <= 0:
            raise ValueError("Period must be > 0")
            
        # 1. Price Difference
        diff_res = calculate_diff(close, timestamps, period=1)
        diff = diff_res.values
        
        # 2. Separate Gains and Losses
        # Note: Math core clip doesn't easily do "clip lower to 0 and upper to inf", but 
        # numpy does. We can just use np.where or np.clip, but to stick to primitives,
        # calculate_clip sets bounds. But wait, `np.where` is faster and directly supported.
        # Since we just need positive and negative arrays, we'll use pure numpy logic here,
        # which is extremely standard for RSI before calling RMA.
        
        gains = np.where(diff > 0, diff, 0.0)
        losses = np.where(diff < 0, -diff, 0.0)
        
        # Handle the nan propagation from diff
        gains[np.isnan(diff)] = np.nan
        losses[np.isnan(diff)] = np.nan
        
        # 3. Wilder's Smoothing (RMA)
        avg_gain_res = calculate_rma(gains, timestamps, period)
        avg_loss_res = calculate_rma(losses, timestamps, period)
        
        avg_gain = avg_gain_res.values
        avg_loss = avg_loss_res.values
        
        # 4. Compute RS and RSI
        with np.errstate(invalid='ignore', divide='ignore'):
            rs = avg_gain / avg_loss
            rsi = np.where(avg_loss == 0, 100.0, 100.0 - (100.0 / (1.0 + rs)))
            
        # 5. Mask
        valid_mask = ~np.isnan(rsi)
        
        # Total warmup = diff (1) + rma warmup (period - 1)
        warmup = period
        
        return RSIResult(
            timestamps=timestamps,
            valid_mask=valid_mask,
            warmup_period=warmup,
            lookback=period + 1,
            metadata={"period": period},
            rsi=rsi
        )
