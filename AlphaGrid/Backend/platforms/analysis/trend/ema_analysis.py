import pandas as pd
from typing import Dict, Any
from Backend.platforms.analysis.factory.factory import BaseAnalysis
from Backend.platforms.analysis.core.dto import AnalysisContext, AnalysisResult

class EMAAnalysis(BaseAnalysis):
    def execute(self, context: AnalysisContext) -> AnalysisResult:
        indicator_engine = context.dependencies.get("indicator_engine")
        if not indicator_engine:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": "Indicator Engine unavailable"})
            
        try:
            ema_20 = indicator_engine.get_indicator("EMA", context.market_data, length=20)
            ema_50 = indicator_engine.get_indicator("EMA", context.market_data, length=50)
            ema_200 = indicator_engine.get_indicator("EMA", context.market_data, length=200)
        except Exception as e:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": str(e)})
            
        if ema_20.empty or ema_50.empty or ema_200.empty:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": "Empty indicator data"})
            
        latest_20 = ema_20.iloc[-1]
        latest_50 = ema_50.iloc[-1]
        latest_200 = ema_200.iloc[-1]
        latest_price = context.market_data['close'].iloc[-1]
        
        classification = "Neutral"
        score = 0.0
        confidence = 0.0
        risk_flags = ["Medium"]
        evidence = [f"EMA20: {latest_20:.2f}", f"EMA50: {latest_50:.2f}", f"EMA200: {latest_200:.2f}"]
        contradictions = []
        
        if latest_20 > latest_50 > latest_200:
            if latest_price > latest_20:
                classification = "Strong Uptrend"
                score = 0.85
                confidence = 0.90
                risk_flags = ["Low"]
                evidence.append("Price > EMA20 > EMA50 > EMA200. Perfect bullish alignment.")
            else:
                classification = "Weakening Uptrend"
                score = 0.50
                confidence = 0.60
                risk_flags = ["High"]
                evidence.append("EMA20 > EMA50 > EMA200")
                contradictions.append("Price fell below EMA20.")
                
        elif latest_20 < latest_50 < latest_200:
            if latest_price < latest_20:
                classification = "Strong Downtrend"
                score = -0.85
                confidence = 0.90
                risk_flags = ["Low"]
                evidence.append("Price < EMA20 < EMA50 < EMA200. Perfect bearish alignment.")
            else:
                classification = "Weakening Downtrend"
                score = -0.50
                confidence = 0.60
                risk_flags = ["High"]
                evidence.append("EMA20 < EMA50 < EMA200")
                contradictions.append("Price broke above EMA20.")
        else:
            classification = "Chop / Range"
            score = 0.0
            confidence = 0.30
            risk_flags = ["High"]
            evidence.append("Moving averages are crossed/tangled.")

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
                "quality": "High",
                "metadata": {"dashboard_widget": "trend_ribbon"}
            }
        )
