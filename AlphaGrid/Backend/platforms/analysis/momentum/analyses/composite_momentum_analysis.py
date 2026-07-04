import pandas as pd
from typing import Dict, Any
from Backend.platforms.analysis.factory import BaseAnalysis
from Backend.platforms.analysis.contracts import AnalysisContext, AnalysisResult
from Backend.platforms.analysis.momentum.analyses.rsi_analysis import RSIAnalysis
from Backend.platforms.analysis.momentum.analyses.macd_analysis import MACDAnalysis

class CompositeMomentumAnalysis(BaseAnalysis):
    def execute(self, context: AnalysisContext) -> AnalysisResult:
        # Resolving dependencies directly from the orchestrator context instead of instantiating sub-analyzers
        rsi_result = context.dependencies.get("ANALYSIS_MOMENTUM_RSI")
        macd_result = context.dependencies.get("ANALYSIS_MOMENTUM_MACD")
        
        if not rsi_result or not macd_result:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": "Sub-analysis dependencies not injected by Orchestrator"})
            
        if rsi_result.metadata.get("status") == "Unsupported" or macd_result.metadata.get("status") == "Unsupported":
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": "One or more sub-analyzers failed"})
            
        rsi_score = rsi_result.score
        macd_score = macd_result.score
        
        score = (rsi_score * 0.4) + (macd_score * 0.6)
        
        classification = "Neutral"
        evidence = [f"RSI Score: {rsi_score:.2f}", f"MACD Score: {macd_score:.2f}"]
        contradictions = []
        
        if rsi_score > 0 and macd_score > 0:
            classification = "Confirmed Bullish Momentum"
            evidence.append("RSI and MACD are both bullish.")
        elif rsi_score < 0 and macd_score < 0:
            classification = "Confirmed Bearish Momentum"
            evidence.append("RSI and MACD are both bearish.")
        else:
            classification = "Mixed Momentum"
            contradictions.append("RSI and MACD disagree on direction.")
            
        return AnalysisResult(
            score=score,
            raw_data=context.market_data,
            signals=[],
            metadata={
                "analysis_type": "momentum",
                "status": "completed",
                "overall_score": score,
                "confidence": 0.85 if len(contradictions) == 0 else 0.40,
                "classification": classification,
                "evidence": evidence,
                "contradictions": contradictions,
                "risk_flags": ["Low" if len(contradictions) == 0 else "High"],
                "quality": "Very High",
                "metadata": {"dashboard_widget": "composite_gauge"}
            }
        )
