import pandas as pd
from typing import Dict, Any
from Backend.platforms.analysis.factory.factory import BaseAnalysis
from Backend.platforms.analysis.core.dto import AnalysisContext, AnalysisResult

class ATRAnalysis(BaseAnalysis):
    def execute(self, context: AnalysisContext) -> AnalysisResult:
        indicator_engine = context.dependencies.get("indicator_engine")
        if not indicator_engine:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": "Indicator Engine unavailable"})
            
        try:
            atr = indicator_engine.get_indicator("ATR", context.market_data, length=14)
        except Exception as e:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": str(e)})
            
        if atr is None or len(atr) < 20: # need some history for relative comparison
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": "Insufficient indicator data"})
            
        curr_atr = atr.iloc[-1]
        
        # Calculate moving average of ATR to determine if volatility is expanding or contracting
        atr_sma = atr.rolling(window=14).mean()
        curr_atr_sma = atr_sma.iloc[-1]
        
        classification = "volatility state: stable"
        score = 0.0
        confidence = 0.60
        risk_flags = ["Medium"]
        evidence = [f"ATR(14): {curr_atr:.2f}", f"ATR SMA(14): {curr_atr_sma:.2f}"]
        contradictions = []
        
        # We classify volatility using the required vocabulary
        if curr_atr > curr_atr_sma * 1.1:
            classification = "expansion"
            score = 0.50 # positive score indicating high volatility (magnitude, not direction)
            evidence.append("ATR is significantly above its average, indicating volatility expansion.")
            risk_flags = ["High"]
        elif curr_atr < curr_atr_sma * 0.8:
            classification = "contraction"
            score = -0.50 # negative score indicating low volatility
            evidence.append("ATR is significantly below its average, indicating volatility contraction.")
            risk_flags = ["Low"]
        else:
            evidence.append("ATR is near its average.")

        return AnalysisResult(
            score=score,
            raw_data=context.market_data,
            signals=[],
            metadata={
                "analysis_type": "volatility",
                "status": "completed",
                "overall_score": score,
                "confidence": confidence,
                "classification": classification,
                "evidence": evidence,
                "contradictions": contradictions,
                "risk_flags": risk_flags,
                "quality": "High",
                "metadata": {"dashboard_widget": "line_chart"}
            }
        )
