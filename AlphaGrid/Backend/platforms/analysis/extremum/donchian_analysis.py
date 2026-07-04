import pandas as pd
from typing import Dict, Any
from Backend.platforms.analysis.factory.factory import BaseAnalysis
from Backend.platforms.analysis.core.dto import AnalysisContext, AnalysisResult

class DonchianAnalysis(BaseAnalysis):
    def execute(self, context: AnalysisContext) -> AnalysisResult:
        indicator_engine = context.dependencies.get("indicator_engine")
        if not indicator_engine:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": "Indicator Engine unavailable"})
            
        try:
            dc = indicator_engine.get_indicator("DONCHIAN", context.market_data)
        except Exception as e:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": str(e)})
            
        if dc is None or len(dc) < 20:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": "Insufficient indicator data"})
            
        # Assuming dc is DataFrame with 'upper', 'lower', 'middle'
        curr_price = context.market_data['close'].iloc[-1]
        upper = dc['upper'].iloc[-1]
        lower = dc['lower'].iloc[-1]
        
        dist_res = upper - curr_price
        dist_sup = curr_price - lower
        
        classification = "channel position: neutral"
        score = 0.0
        confidence = 0.60
        risk_flags = ["Medium"]
        evidence = [f"Distance to resistance: {dist_res:.2f}", f"Distance to support: {dist_sup:.2f}"]
        contradictions = []
        
        if curr_price >= upper * 0.99:
            classification = "breakout pressure: high (resistance)"
            score = 0.70
            risk_flags = ["High"]
            evidence.append("Price is testing upper Donchian channel.")
        elif curr_price <= lower * 1.01:
            classification = "breakout pressure: high (support)"
            score = -0.70
            risk_flags = ["High"]
            evidence.append("Price is testing lower Donchian channel.")

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
                "metadata": {"dashboard_widget": "channel_chart"}
            }
        )
