import os
import pandas as pd
from typing import Dict, Any
from Backend.platforms.analysis.factory.factory import BaseAnalysis
from Backend.platforms.analysis.core.dto import AnalysisContext, AnalysisResult

class RSIAnalysis(BaseAnalysis):
    def execute(self, context: AnalysisContext) -> AnalysisResult:
        indicator_engine = context.dependencies.get("indicator_engine")
        if not indicator_engine:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": "Indicator Engine unavailable"})
            
        try:
            rsi_14 = indicator_engine.get_indicator("RSI", context.market_data, length=14)
        except Exception as e:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": f"Required indicators unavailable: {str(e)}"})
            
        if rsi_14.empty:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": "Empty indicator data"})
            
        latest_rsi = rsi_14.iloc[-1]
        
        classification = "Neutral"
        score = 0.0
        confidence = 0.50
        risk_flags = ["Medium"]
        evidence = [f"RSI(14): {latest_rsi:.2f}"]
        contradictions = []
        
        if latest_rsi > 70:
            classification = "Overbought"
            score = -0.70  # Momentum is high, but price is stretched
            confidence = 0.80
            risk_flags = ["High (Reversal Risk)"]
            evidence.append("RSI is strictly above the 70 overbought threshold.")
        elif latest_rsi < 30:
            classification = "Oversold"
            score = 0.70
            confidence = 0.80
            risk_flags = ["High (Reversal Risk)"]
            evidence.append("RSI is strictly below the 30 oversold threshold.")
        elif 50 <= latest_rsi <= 70:
            classification = "Bullish Momentum"
            score = 0.50
            risk_flags = ["Low"]
            evidence.append("RSI is in the bullish zone (50-70).")
        elif 30 <= latest_rsi < 50:
            classification = "Bearish Momentum"
            score = -0.50
            risk_flags = ["Low"]
            evidence.append("RSI is in the bearish zone (30-50).")

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
                "metadata": {"dashboard_widget": "oscillator"}
            }
        )
