from Backend.platforms.analysis.core.BaseAnalysis import BaseAnalysis
from Backend.platforms.analysis.core.AnalysisContext import AnalysisContext
from Backend.platforms.analysis.core.AnalysisResult import AnalysisResult
from Backend.platforms.analysis.core.AnalysisRegistry import AnalysisRegistration

class MACDTrendAnalysis(BaseAnalysis):
    """
    Analyzes trend state and momentum exhaustion based on MACD line and Histogram.
    DOES NOT GENERATE SIGNALS (BUY/SELL). Purely descriptive.
    """
    
    def get_registration(self) -> AnalysisRegistration:
        return AnalysisRegistration(
            id="tech_trend_macd_001",
            name="MACDTrendAnalysis",
            category="Technical",
            subcategory="Trend",
            version="1.0.0",
            required_indicators=["MACD_Line", "MACD_Signal", "MACD_Hist"],
            required_markets=["Crypto", "Stocks", "Forex"],
            supported_timeframes=["15m", "1h", "4h", "1d"],
            supported_trading_styles=["Trend Following", "Swing"],
            output_fields=["macd_trend", "histogram_state", "divergence_warning"],
            dashboard_widgets=["MACD State Indicator"],
            ai_compatibility=True,
            documentation="Evaluates trend direction via MACD zero-line cross and histogram expansions/contractions."
        )

    def execute(self, context: AnalysisContext) -> AnalysisResult:
        indicators = context.indicators
        
        macd_line = indicators.get("MACD_Line")
        macd_signal = indicators.get("MACD_Signal")
        macd_hist = indicators.get("MACD_Hist")
        
        direction = "NEUTRAL"
        hist_state = "FLAT"
        warnings = []
        score = 0.0
        
        if macd_line is not None and macd_signal is not None and macd_hist is not None:
            # Determine Base Trend Direction from Zero Line
            if macd_line > 0:
                direction = "BULLISH"
                score = 50.0
            elif macd_line < 0:
                direction = "BEARISH"
                score = -50.0
                
            # Determine momentum/expansion from Histogram
            if macd_hist > 0:
                if macd_hist > 1.0: # simplistic proxy for expanding positive
                    hist_state = "EXPANDING_POSITIVE"
                    score += 30.0
                else:
                    hist_state = "CONTRACTING_POSITIVE"
                    score += 10.0
            elif macd_hist < 0:
                if macd_hist < -1.0: # proxy for expanding negative
                    hist_state = "EXPANDING_NEGATIVE"
                    score -= 30.0
                else:
                    hist_state = "CONTRACTING_NEGATIVE"
                    score -= 10.0
                    
            if macd_line > 0 and hist_state == "CONTRACTING_POSITIVE":
                warnings.append("Bullish MACD trend but momentum is contracting (possible exhaustion).")
        else:
            warnings.append("Missing required MACD indicators.")
            
        result = AnalysisResult(
            analysis_type=self.get_registration().name,
            market=context.market,
            symbol=context.symbol,
            timeframe=context.timeframe,
            status="SUCCESS",
            confidence=85.0 if len(warnings) == 0 else 50.0,
            numeric_score=score,
            normalized_score=score / 100.0,
            supporting_indicators=self.get_registration().required_indicators,
            warnings=warnings,
            metadata={
                "macd_trend": direction,
                "histogram_state": hist_state
            },
            ai_metadata={
                "explanation_template": "MACD trend is {macd_trend} with {histogram_state} momentum.",
                "assumptions": ["Assumes MACD standard settings (12, 26, 9)."],
                "limitations": ["Prone to whipsaws in ranging markets."]
            },
            evidence=f"MACD_Line: {macd_line}, Signal: {macd_signal}, Hist: {macd_hist}"
        )
        
        return result
