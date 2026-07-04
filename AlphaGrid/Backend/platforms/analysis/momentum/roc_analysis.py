import pandas as pd
from typing import Dict, Any
from Backend.platforms.analysis.factory.factory import BaseAnalysis
from Backend.platforms.analysis.core.dto import AnalysisContext, AnalysisResult

class ROCAnalysis(BaseAnalysis):
    def execute(self, context: AnalysisContext) -> AnalysisResult:
        indicator_engine = context.dependencies.get("indicator_engine")
        if not indicator_engine:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": "Indicator Engine unavailable"})
            
        try:
            roc_9 = indicator_engine.get_indicator("ROC", context.market_data, length=9)
        except Exception as e:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": f"Required indicators unavailable: {str(e)}"})
            
        if roc_9.empty:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": "Empty indicator data"})
            
        latest_roc = roc_9.iloc[-1]
        
        classification = "Neutral"
        score = 0.0
        confidence = 0.50
        risk_flags = ["Medium"]
        evidence = [f"ROC(9): {latest_roc:.2f}"]
        contradictions = []
        
        if latest_roc > 0:
            classification = "Positive Momentum"
            score = 0.60
            confidence = 0.70
            risk_flags = ["Low"]
            evidence.append("ROC is above the zero line, indicating acceleration in price.")
        elif latest_roc < 0:
            classification = "Negative Momentum"
            score = -0.60
            confidence = 0.70
            risk_flags = ["Low"]
            evidence.append("ROC is below the zero line, indicating deceleration in price.")
        else:
            evidence.append("ROC is exactly zero.")

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
                "metadata": {"dashboard_widget": "bar_chart"}
            }
        )
