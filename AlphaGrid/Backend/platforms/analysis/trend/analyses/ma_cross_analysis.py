import pandas as pd
from typing import Dict, Any
from Backend.platforms.analysis.factory import BaseAnalysis
from Backend.platforms.analysis.contracts import AnalysisContext, AnalysisResult

class MACrossAnalysis(BaseAnalysis):
    def execute(self, context: AnalysisContext) -> AnalysisResult:
        indicator_engine = context.dependencies.get("indicator_engine")
        if not indicator_engine:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": "Indicator Engine unavailable"})
            
        try:
            sma_50 = indicator_engine.get_indicator("SMA", context.market_data, length=50)
            sma_200 = indicator_engine.get_indicator("SMA", context.market_data, length=200)
        except Exception as e:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": str(e)})
            
        if len(sma_50) < 2 or len(sma_200) < 2:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": "Insufficient data for cross"})
            
        curr_50, prev_50 = sma_50.iloc[-1], sma_50.iloc[-2]
        curr_200, prev_200 = sma_200.iloc[-1], sma_200.iloc[-2]
        
        classification = "Neutral"
        score = 0.0
        confidence = 0.50
        risk_flags = ["Medium"]
        evidence = [f"50SMA: {curr_50:.2f}", f"200SMA: {curr_200:.2f}"]
        
        if prev_50 <= prev_200 and curr_50 > curr_200:
            classification = "Golden Cross (Bullish Reversal)"
            score = 0.90
            confidence = 0.95
            risk_flags = ["Low"]
            evidence.append("50 SMA just crossed ABOVE 200 SMA.")
        elif prev_50 >= prev_200 and curr_50 < curr_200:
            classification = "Death Cross (Bearish Reversal)"
            score = -0.90
            confidence = 0.95
            risk_flags = ["Low"]
            evidence.append("50 SMA just crossed BELOW 200 SMA.")
        elif curr_50 > curr_200:
            classification = "Uptrend"
            score = 0.50
            evidence.append("50 SMA is above 200 SMA (no recent cross).")
        else:
            classification = "Downtrend"
            score = -0.50
            evidence.append("50 SMA is below 200 SMA (no recent cross).")
            
        return AnalysisResult(
            score=score,
            raw_data=context.market_data,
            signals=[],
            metadata={
                "analysis_type": "trend",
                "status": "completed",
                "overall_score": score,
                "confidence": confidence,
                "classification": classification,
                "evidence": evidence,
                "contradictions": [],
                "risk_flags": risk_flags,
                "quality": "Very High",
                "metadata": {}
            }
        )
