import pandas as pd
from typing import Dict, Any
from Backend.platforms.analysis.factory import BaseAnalysis
from Backend.platforms.analysis.contracts import AnalysisContext, AnalysisResult

class HighLowAnalysis(BaseAnalysis):
    def execute(self, context: AnalysisContext) -> AnalysisResult:
        indicator_engine = context.dependencies.get("indicator_engine")
        if not indicator_engine:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": "Indicator Engine unavailable"})
            
        try:
            hl = indicator_engine.get_indicator("HIGHLOW", context.market_data)
        except Exception as e:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": str(e)})
            
        if hl is None or len(hl) < 20:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": "Insufficient indicator data"})
            
        curr_price = context.market_data['close'].iloc[-1]
        highest_high = hl['highest'].iloc[-1]
        lowest_low = hl['lowest'].iloc[-1]
        
        dist_res = highest_high - curr_price
        dist_sup = curr_price - lowest_low
        
        classification = "channel position: mid"
        score = 0.0
        confidence = 0.50
        risk_flags = ["Medium"]
        evidence = [f"Distance to resistance: {dist_res:.2f}", f"Distance to support: {dist_sup:.2f}"]
        contradictions = []
        
        if curr_price >= highest_high * 0.98:
            classification = "breakout pressure: resistance test"
            score = 0.50
            evidence.append("Price is near recent highs.")
        elif curr_price <= lowest_low * 1.02:
            classification = "breakout pressure: support test"
            score = -0.50
            evidence.append("Price is near recent lows.")

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
                "metadata": {"dashboard_widget": "range_chart"}
            }
        )
