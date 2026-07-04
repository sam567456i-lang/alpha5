import pandas as pd
from typing import Dict, Any
from Backend.platforms.analysis.factory.factory import BaseAnalysis
from Backend.platforms.analysis.core.dto import AnalysisContext, AnalysisResult

class VWAPAnalysis(BaseAnalysis):
    def execute(self, context: AnalysisContext) -> AnalysisResult:
        indicator_engine = context.dependencies.get("indicator_engine")
        if not indicator_engine:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": "Indicator Engine unavailable"})
            
        try:
            vwap = indicator_engine.get_indicator("VWAP", context.market_data)
        except Exception as e:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": str(e)})
            
        if vwap is None or len(vwap) == 0:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": "Insufficient indicator data"})
            
        curr_price = context.market_data['close'].iloc[-1]
        curr_vwap = vwap.iloc[-1]
        
        classification = "participation: neutral"
        score = 0.0
        confidence = 0.60
        risk_flags = ["Medium"]
        evidence = [f"Price: {curr_price:.2f}", f"VWAP: {curr_vwap:.2f}"]
        contradictions = []
        
        if curr_price > curr_vwap * 1.005:
            classification = "accumulation"
            score = 0.60
            risk_flags = ["Low"]
            evidence.append("Price is holding above VWAP, suggesting institutional accumulation.")
        elif curr_price < curr_vwap * 0.995:
            classification = "distribution"
            score = -0.60
            risk_flags = ["Low"]
            evidence.append("Price is holding below VWAP, suggesting institutional distribution.")

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
                "metadata": {"dashboard_widget": "vwap_chart"}
            }
        )
