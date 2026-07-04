import pandas as pd
from typing import Dict, Any
from Backend.platforms.analysis.factory.factory import BaseAnalysis
from Backend.platforms.analysis.core.dto import AnalysisContext, AnalysisResult

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
        
        trend_state = "Neutral"
        score = 0.0
        confidence = 0.50
        risk = "Medium"
        evidence = f"50SMA: {curr_50:.2f}, 200SMA: {curr_200:.2f}"
        
        if prev_50 <= prev_200 and curr_50 > curr_200:
            trend_state = "Golden Cross (Bullish Reversal)"
            score = 0.90
            confidence = 0.95
            risk = "Low"
            evidence = "50 SMA just crossed ABOVE 200 SMA."
        elif prev_50 >= prev_200 and curr_50 < curr_200:
            trend_state = "Death Cross (Bearish Reversal)"
            score = -0.90
            confidence = 0.95
            risk = "Low"
            evidence = "50 SMA just crossed BELOW 200 SMA."
        elif curr_50 > curr_200:
            trend_state = "Uptrend"
            score = 0.50
            evidence = "50 SMA is above 200 SMA (no recent cross)."
        else:
            trend_state = "Downtrend"
            score = -0.50
            evidence = "50 SMA is below 200 SMA (no recent cross)."
            
        return AnalysisResult(score, context.market_data, [], {
            "status": "Success", "trend": trend_state, "confidence": confidence,
            "evidence": evidence, "risk": risk, "contradictions": "None", "quality": "Very High"
        })
