"""Market Regime Detector — rule-based regime classification."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


class RegimeDetector:
    """Classifies the market regime using rules on breadth, VIX, and trend."""

    @staticmethod
    def detect_regime(
        breadth_score: float,
        vix_value: float,
        trend_strength: float = 0.5,  # 0 to 1, where >0.6 is strong
    ) -> dict[str, str | float]:
        """Detect the market regime.
        
        Args:
            breadth_score: 0.0 to 1.0 (from MarketBreadthCalculator)
            vix_value: India VIX value (e.g. 15.2)
            trend_strength: Optional trend strength metric (e.g. ADX/100)
            
        Returns:
            Dict containing regime, confidence, and volatility_score.
        """
        regime = "RANGE_BOUND"
        confidence = 0.5
        
        # Volatility assessment
        if vix_value > 25.0:
            volatility = "HIGH"
            vol_score = 1.0
        elif vix_value < 12.0:
            volatility = "LOW"
            vol_score = 0.0
        else:
            volatility = "NORMAL"
            vol_score = (vix_value - 12.0) / 13.0

        # Regime rules
        if volatility == "HIGH" and trend_strength < 0.4:
            regime = "HIGH_VOLATILITY"
            confidence = 0.8
        elif breadth_score > 0.65 and trend_strength > 0.5:
            regime = "TRENDING_BULLISH"
            confidence = min(0.9, breadth_score)
        elif breadth_score < 0.35 and trend_strength > 0.5:
            regime = "TRENDING_BEARISH"
            confidence = min(0.9, 1.0 - breadth_score)
        elif breadth_score > 0.8:
            regime = "BREAKOUT"
            confidence = 0.85
        elif volatility == "LOW" and 0.4 < breadth_score < 0.6:
            regime = "LOW_VOLATILITY"
            confidence = 0.7
        else:
            regime = "RANGE_BOUND"
            # Confidence is higher when breadth is closer to 0.5
            confidence = 1.0 - abs(breadth_score - 0.5) * 2

        return {
            "regime": regime,
            "confidence": round(confidence, 2),
            "volatility_score": round(vol_score, 2),
            "trend_strength": round(trend_strength, 2),
        }
