import pandas as pd
from typing import Dict, Any
from Backend.platforms.analysis.factory.factory import BaseAnalysis
from Backend.platforms.analysis.core.dto import AnalysisContext, AnalysisResult

class WMAAnalysis(BaseAnalysis):
    def execute(self, context: AnalysisContext) -> AnalysisResult:
        indicator_engine = context.dependencies.get("indicator_engine")
        if not indicator_engine:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": "Indicator Engine unavailable"})
            
        try:
            wma_20 = indicator_engine.get_indicator("WMA", context.market_data, length=20)
            wma_50 = indicator_engine.get_indicator("WMA", context.market_data, length=50)
            wma_200 = indicator_engine.get_indicator("WMA", context.market_data, length=200)
        except Exception as e:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": str(e)})
            
        if wma_20.empty or wma_50.empty or wma_200.empty:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": "Empty indicator data"})
            
        latest_20 = wma_20.iloc[-1]
        latest_50 = wma_50.iloc[-1]
        latest_200 = wma_200.iloc[-1]
        
        classification = "Neutral"
        score = 0.0
        confidence = 0.20
        risk_flags = ["Medium"]
        evidence = [f"WMA20: {latest_20:.2f}", f"WMA50: {latest_50:.2f}", f"WMA200: {latest_200:.2f}"]
        
        if latest_20 > latest_50 > latest_200:
            classification = "Strong Uptrend"
            score = 0.85
            confidence = 0.90
            risk_flags = ["Low"]
            evidence.append("Bullish alignment.")
        elif latest_20 < latest_50 < latest_200:
            classification = "Strong Downtrend"
            score = -0.85
            confidence = 0.90
            risk_flags = ["Low"]
            evidence.append("Bearish alignment.")
            
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
                "quality": "High",
                "metadata": {}
            }
        )
