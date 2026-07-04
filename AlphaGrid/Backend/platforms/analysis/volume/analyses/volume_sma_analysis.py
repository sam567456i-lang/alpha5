import pandas as pd
from typing import Dict, Any
from Backend.platforms.analysis.factory import BaseAnalysis
from Backend.platforms.analysis.contracts import AnalysisContext, AnalysisResult

class VolumeSMAAnalysis(BaseAnalysis):
    def execute(self, context: AnalysisContext) -> AnalysisResult:
        indicator_engine = context.dependencies.get("indicator_engine")
        if not indicator_engine:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": "Indicator Engine unavailable"})
            
        try:
            vsma = indicator_engine.get_indicator("VOLUME_SMA", context.market_data, length=20)
        except Exception as e:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": str(e)})
            
        if vsma is None or len(vsma) == 0:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": "Insufficient indicator data"})
            
        curr_vol = context.market_data['volume'].iloc[-1]
        curr_sma = vsma.iloc[-1]
        
        classification = "participation: average"
        score = 0.0
        confidence = 0.50
        risk_flags = ["Medium"]
        evidence = [f"Volume: {curr_vol:.0f}", f"Vol SMA: {curr_sma:.0f}"]
        contradictions = []
        
        if curr_vol > curr_sma * 1.5:
            classification = "volume confirmation"
            score = 0.60
            evidence.append("Volume is significantly above average, confirming participation.")
            risk_flags = ["Low"]
        elif curr_vol < curr_sma * 0.5:
            classification = "volume weakness"
            score = -0.60
            evidence.append("Volume is significantly below average, indicating weak participation.")
            risk_flags = ["High"]

        return AnalysisResult(
            score=score,
            raw_data=context.market_data,
            signals=[],
            metadata={
                "analysis_type": "volume",
                "status": "completed",
                "overall_score": score,
                "confidence": confidence,
                "classification": classification,
                "evidence": evidence,
                "contradictions": contradictions,
                "risk_flags": risk_flags,
                "quality": "High",
                "metadata": {"dashboard_widget": "volume_bars"}
            }
        )
