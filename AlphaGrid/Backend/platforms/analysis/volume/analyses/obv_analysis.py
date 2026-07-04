import pandas as pd
from typing import Dict, Any
from Backend.platforms.analysis.factory import BaseAnalysis
from Backend.platforms.analysis.contracts import AnalysisContext, AnalysisResult

class OBVAnalysis(BaseAnalysis):
    def execute(self, context: AnalysisContext) -> AnalysisResult:
        indicator_engine = context.dependencies.get("indicator_engine")
        if not indicator_engine:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": "Indicator Engine unavailable"})
            
        try:
            obv = indicator_engine.get_indicator("OBV", context.market_data)
        except Exception as e:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": str(e)})
            
        if obv is None or len(obv) < 20:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": "Insufficient indicator data"})
            
        obv_sma = obv.rolling(window=20).mean()
        curr_obv = obv.iloc[-1]
        curr_sma = obv_sma.iloc[-1]
        
        classification = "participation: neutral"
        score = 0.0
        confidence = 0.65
        risk_flags = ["Medium"]
        evidence = [f"OBV vs SMA: {curr_obv:.2f} / {curr_sma:.2f}"]
        contradictions = []
        
        if curr_obv > curr_sma:
            classification = "volume confirmation"
            score = 0.50
            evidence.append("OBV is above its moving average, confirming upside participation.")
        else:
            classification = "volume weakness"
            score = -0.50
            evidence.append("OBV is below its moving average, confirming downside participation or weakness.")

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
                "metadata": {"dashboard_widget": "obv_chart"}
            }
        )
