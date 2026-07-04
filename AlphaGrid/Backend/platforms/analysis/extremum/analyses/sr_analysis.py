import pandas as pd
from typing import Dict, Any
from Backend.platforms.analysis.factory import BaseAnalysis
from Backend.platforms.analysis.contracts import AnalysisContext, AnalysisResult

class SupportResistanceAnalysis(BaseAnalysis):
    def execute(self, context: AnalysisContext) -> AnalysisResult:
        indicator_engine = context.dependencies.get("indicator_engine")
        if not indicator_engine:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": "Indicator Engine unavailable"})
            
        try:
            sr = indicator_engine.get_indicator("SR", context.market_data)
        except Exception as e:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": str(e)})
            
        if sr is None or len(sr) == 0:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": "Insufficient indicator data"})
            
        # Assuming sr returns a dict or dataframe of closest S/R levels
        curr_price = context.market_data['close'].iloc[-1]
        resistance = sr['resistance'].iloc[-1]
        support = sr['support'].iloc[-1]
        
        dist_res = resistance - curr_price
        dist_sup = curr_price - support
        
        classification = "channel position: floating"
        score = 0.0
        confidence = 0.75
        risk_flags = ["Medium"]
        evidence = [f"Distance to resistance: {dist_res:.2f}", f"Distance to support: {dist_sup:.2f}"]
        contradictions = []
        
        # If very close to resistance, breakout pressure is high
        if dist_res < (curr_price * 0.01):
            classification = "breakout pressure: critical resistance"
            score = 0.80
            risk_flags = ["High"]
            evidence.append("Price is within 1% of major resistance.")
        elif dist_sup < (curr_price * 0.01):
            classification = "breakout pressure: critical support"
            score = -0.80
            risk_flags = ["High"]
            evidence.append("Price is within 1% of major support.")

        return AnalysisResult(
            score=score,
            raw_data=context.market_data,
            signals=[],
            metadata={
                "analysis_type": "extremum",
                "status": "completed",
                "overall_score": score,
                "confidence": confidence,
                "classification": classification,
                "evidence": evidence,
                "contradictions": contradictions,
                "risk_flags": risk_flags,
                "quality": "High",
                "metadata": {"dashboard_widget": "levels_chart"}
            }
        )
