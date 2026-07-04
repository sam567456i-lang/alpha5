import pandas as pd
from typing import Dict, Any
from Backend.platforms.analysis.factory import BaseAnalysis
from Backend.platforms.analysis.contracts import AnalysisContext, AnalysisResult

class SMAAnalysis(BaseAnalysis):
    def execute(self, context: AnalysisContext) -> AnalysisResult:
        indicator_engine = context.dependencies.get("indicator_engine")
        if not indicator_engine:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": "Indicator Engine unavailable"})
            
        try:
            sma_20 = indicator_engine.get_indicator("SMA", context.market_data, length=20)
            sma_50 = indicator_engine.get_indicator("SMA", context.market_data, length=50)
            sma_200 = indicator_engine.get_indicator("SMA", context.market_data, length=200)
        except Exception as e:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": str(e)})
            
        if sma_20.empty or sma_50.empty or sma_200.empty:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": "Empty indicator data"})
            
        latest_20 = sma_20.iloc[-1]
        latest_50 = sma_50.iloc[-1]
        latest_200 = sma_200.iloc[-1]
        latest_price = context.market_data['close'].iloc[-1]
        
        classification = "Neutral"
        score = 0.0
        confidence = 0.0
        risk_flags = ["Medium"]
        evidence = [f"SMA20: {latest_20:.2f}", f"SMA50: {latest_50:.2f}", f"SMA200: {latest_200:.2f}"]
        contradictions = []
        
        if latest_20 > latest_50 > latest_200:
            if latest_price > latest_20:
                classification = "Strong Uptrend"
                score = 0.80
                confidence = 0.85
                risk_flags = ["Low"]
                evidence.append("Bullish alignment.")
            else:
                classification = "Weakening Uptrend"
                score = 0.40
                confidence = 0.50
                risk_flags = ["High"]
                contradictions.append("Price fell below SMA20.")
                
        elif latest_20 < latest_50 < latest_200:
            if latest_price < latest_20:
                classification = "Strong Downtrend"
                score = -0.80
                confidence = 0.85
                risk_flags = ["Low"]
                evidence.append("Bearish alignment.")
            else:
                classification = "Weakening Downtrend"
                score = -0.40
                confidence = 0.50
                risk_flags = ["High"]
                contradictions.append("Price broke above SMA20.")
        else:
            classification = "Chop / Range"
            score = 0.0
            confidence = 0.20
            risk_flags = ["High"]
            evidence.append("SMAs are tangled.")

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
                "contradictions": contradictions,
                "risk_flags": risk_flags,
                "quality": "Medium",
                "metadata": {}
            }
        )
