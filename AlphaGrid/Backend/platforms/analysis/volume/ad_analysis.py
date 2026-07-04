import pandas as pd
from typing import Dict, Any
from Backend.platforms.analysis.factory.factory import BaseAnalysis
from Backend.platforms.analysis.core.dto import AnalysisContext, AnalysisResult

class AccumulationDistributionAnalysis(BaseAnalysis):
    def execute(self, context: AnalysisContext) -> AnalysisResult:
        indicator_engine = context.dependencies.get("indicator_engine")
        if not indicator_engine:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": "Indicator Engine unavailable"})
            
        try:
            ad = indicator_engine.get_indicator("ACC_DIST", context.market_data)
        except Exception as e:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": str(e)})
            
        if ad is None or len(ad) < 2:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": "Insufficient indicator data"})
            
        curr_ad = ad.iloc[-1]
        prev_ad = ad.iloc[-2]
        
        classification = "participation: neutral"
        score = 0.0
        confidence = 0.60
        risk_flags = ["Medium"]
        evidence = [f"A/D Line Trend: {curr_ad:.2f} vs {prev_ad:.2f}"]
        contradictions = []
        
        if curr_ad > prev_ad:
            classification = "accumulation"
            score = 0.55
            evidence.append("A/D line is rising, showing accumulation.")
        elif curr_ad < prev_ad:
            classification = "distribution"
            score = -0.55
            evidence.append("A/D line is falling, showing distribution.")

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
                "metadata": {"dashboard_widget": "ad_line"}
            }
        )
