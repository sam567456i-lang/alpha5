import numpy as np
from Backend.indicator_engine.results import FinancialIndicatorResult
from dataclasses import dataclass
from Backend.indicator_engine.momentum.rsi import RSIEngine
from Backend.math.public.roc import calculate_roc
from Backend.indicator_engine.momentum.macd import MACDEngine
from Backend.market_data.market_series import MarketSeries

@dataclass(frozen=True)
class MomentumEngineResult(FinancialIndicatorResult):
    momentum_score: np.ndarray # Composite score from -100 to 100
    rsi_component: np.ndarray
    roc_component: np.ndarray
    macd_component: np.ndarray

class MomentumEngine:
    """
    Composite Momentum Engine.
    Fuses RSI, ROC, and MACD normalized into a single bounded momentum score (-100 to 100).
    """
    @staticmethod
    def compute(close: np.ndarray, timestamps: np.ndarray, rsi_period: int = 14, roc_period: int = 14, fast_period: int = 12, slow_period: int = 26) -> MomentumEngineResult:
        # 1. RSI Component (0 to 100) -> scale to -100 to 100
        rsi_res = RSIEngine.compute(close, timestamps, rsi_period)
        rsi_comp = (rsi_res.rsi - 50.0) * 2.0
        
        # 2. ROC Component
        roc_res = calculate_roc(close, timestamps, roc_period, "close")
        # Normalize ROC roughly to -100 to 100 (assume typical max ROC is 10% over period)
        roc_comp = np.clip(roc_res.values * 1000.0, -100.0, 100.0)
        
        # 3. MACD Component
        mock_series = MarketSeries(timestamps=timestamps, closes=close, opens=close, highs=close, lows=close, volumes=close)
        macd_engine = MACDEngine(fast_period, slow_period, 9)
        macd_res = macd_engine.generate(mock_series)
        # Normalize MACD Histogram
        hist = macd_res.histogram
        # Dynamic volatility-based scaling would be better, but we use a simple rolling max abs for normalization
        n = len(close)
        macd_comp = np.zeros(n)
        for i in range(1, n):
            if not np.isnan(hist[i]):
                # simple proxy for max expected hist
                max_hist = max(0.0001, np.nanmax(np.abs(hist[max(0, i-100):i+1])))
                macd_comp[i] = (hist[i] / max_hist) * 100.0
                
        # 4. Composite Score
        with np.errstate(invalid='ignore'):
            momentum_score = (rsi_comp * 0.4) + (roc_comp * 0.3) + (macd_comp * 0.3)
            momentum_score = np.clip(momentum_score, -100.0, 100.0)
            
        valid_mask = ~np.isnan(momentum_score)
        warmup = max(rsi_period, roc_period, slow_period + 9)
        
        return MomentumEngineResult(
            timestamps=timestamps,
            valid_mask=valid_mask,
            warmup_period=warmup,
            lookback=warmup,
            metadata={"indicator": "Momentum Engine"},
            momentum_score=momentum_score,
            rsi_component=rsi_comp,
            roc_component=roc_comp,
            macd_component=macd_comp
        )
