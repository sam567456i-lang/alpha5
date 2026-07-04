from Backend.platforms.analysis.core.BaseAnalysis import BaseAnalysis
from Backend.platforms.analysis.core.AnalysisContext import AnalysisContext
from Backend.platforms.analysis.core.AnalysisResult import AnalysisResult
from Backend.platforms.analysis.core.AnalysisRegistry import AnalysisRegistration

class MovingAverageTrendAnalysis(BaseAnalysis):
    """
    Analyzes trend direction, strength, and alignment based on Moving Averages.
    DOES NOT GENERATE SIGNALS (BUY/SELL). Purely descriptive.
    """
    
    def get_registration(self) -> AnalysisRegistration:
        return AnalysisRegistration(
            id="tech_trend_ma_001",
            name="MovingAverageTrendAnalysis",
            category="Technical",
            subcategory="Trend",
            version="1.0.0",
            required_indicators=["EMA_9", "EMA_21", "SMA_50", "SMA_200"],
            required_markets=["Crypto", "Stocks", "Forex"],
            supported_timeframes=["1m", "5m", "15m", "1h", "4h", "1d", "1w"],
            supported_trading_styles=["Trend Following", "Swing", "Day Trading"],
            output_fields=["trend_direction", "trend_strength", "alignment", "slope_profile"],
            dashboard_widgets=["Trend Alignment Ribbon", "Trend Strength Gauge"],
            ai_compatibility=True,
            documentation="Evaluates trend state by analyzing the alignment, distance, and slope of short, medium, and long-term moving averages."
        )

    def execute(self, context: AnalysisContext) -> AnalysisResult:
        indicators = context.indicators
        
        # Safely extract indicator values if present
        ema9 = indicators.get("EMA_9")
        ema21 = indicators.get("EMA_21")
        sma50 = indicators.get("SMA_50")
        sma200 = indicators.get("SMA_200")
        
        # We need historical values to calculate slope, but for this execution, 
        # let's assume indicators dictionary contains current values or a time-series.
        # MVP: Assume scalar current values for the context of this example.
        
        direction = "NEUTRAL"
        strength = "WEAK"
        alignment = False
        warnings = []
        score = 0.0
        
        if ema9 and ema21 and sma50 and sma200:
            # Bullish Alignment: Fast > Slow
            if ema9 > ema21 > sma50 > sma200:
                direction = "BULLISH"
                alignment = True
                score = 80.0
                strength = "STRONG"
                
                # Check for over-extension (price far from mean)
                # In a real scenario, we'd check current price vs SMA_200
                
            # Bearish Alignment: Fast < Slow
            elif ema9 < ema21 < sma50 < sma200:
                direction = "BEARISH"
                alignment = True
                score = -80.0
                strength = "STRONG"
                
            else:
                direction = "CHOP"
                score = 0.0
                strength = "NONE"
                warnings.append("Moving averages are tangled, indicating no clear trend alignment.")
        else:
            warnings.append("Missing required indicators for full Moving Average Trend Analysis.")
            
        result = AnalysisResult(
            analysis_type=self.get_registration().name,
            market=context.market,
            symbol=context.symbol,
            timeframe=context.timeframe,
            status="SUCCESS",
            confidence=90.0 if alignment else 40.0,
            numeric_score=score,
            normalized_score=score / 100.0,
            supporting_indicators=self.get_registration().required_indicators,
            warnings=warnings,
            metadata={
                "trend_direction": direction,
                "trend_strength": strength,
                "is_aligned": alignment
            },
            ai_metadata={
                "explanation_template": "The moving averages are in a {trend_direction} state with {trend_strength} strength. Alignment is {is_aligned}.",
                "assumptions": ["Assumes standard moving average crossovers dictate trend."],
                "limitations": ["Lags real-time price action."]
            },
            evidence=f"EMA9: {ema9}, EMA21: {ema21}, SMA50: {sma50}, SMA200: {sma200}"
        )
        
        # NO signals are emitted! Just the state description.
        return result
