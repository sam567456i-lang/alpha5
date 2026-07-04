import pandas as pd
from typing import Dict, Any
from Backend.platforms.analysis.factory.factory import BaseAnalysis
from Backend.platforms.analysis.core.dto import AnalysisContext, AnalysisResult

class MACDAnalysis(BaseAnalysis):
    def execute(self, context: AnalysisContext) -> AnalysisResult:
        indicator_engine = context.dependencies.get("indicator_engine")
        if not indicator_engine:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": "Indicator Engine unavailable"})
            
        try:
            macd = indicator_engine.get_indicator("MACD", context.market_data)
        except Exception as e:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": str(e)})
            
        if macd is None or len(macd) < 2:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": "Empty indicator data"})
            
        # Assuming MACD returns a DataFrame with 'macd', 'signal', 'hist'
        curr_macd = macd['macd'].iloc[-1]
        curr_signal = macd['signal'].iloc[-1]
        curr_hist = macd['hist'].iloc[-1]
        prev_hist = macd['hist'].iloc[-2]
        
        classification = "Neutral"
        score = 0.0
        confidence = 0.50
        risk_flags = ["Medium"]
        evidence = [f"MACD: {curr_macd:.2f}", f"Signal: {curr_signal:.2f}", f"Hist: {curr_hist:.2f}"]
        contradictions = []
        
        if curr_macd > curr_signal:
            if curr_hist > prev_hist:
                classification = "Strong Bullish Momentum"
                score = 0.80
                confidence = 0.85
                risk_flags = ["Low"]
                evidence.append("MACD is above Signal and Histogram is expanding.")
            else:
                classification = "Weakening Bullish Momentum"
                score = 0.40
                confidence = 0.60
                risk_flags = ["Medium"]
                evidence.append("MACD is above Signal but Histogram is shrinking.")
        elif curr_macd < curr_signal:
            if curr_hist < prev_hist:
                classification = "Strong Bearish Momentum"
                score = -0.80
                confidence = 0.85
                risk_flags = ["Low"]
                evidence.append("MACD is below Signal and Histogram is expanding negatively.")
            else:
                classification = "Weakening Bearish Momentum"
                score = -0.40
                confidence = 0.60
                risk_flags = ["Medium"]
                evidence.append("MACD is below Signal but Histogram is shrinking.")

        return AnalysisResult(
            score=score,
            raw_data=context.market_data,
            signals=[],
            metadata={
                "analysis_type": "momentum",
                "status": "completed",
                "overall_score": score,
                "confidence": confidence,
                "classification": classification,
                "evidence": evidence,
                "contradictions": contradictions,
                "risk_flags": risk_flags,
                "quality": "High",
                "metadata": {"dashboard_widget": "macd_histogram"}
            }
        )
