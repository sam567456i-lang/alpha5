import pandas as pd
from typing import Dict, Any
from Backend.platforms.analysis.factory.factory import BaseAnalysis
from Backend.platforms.analysis.core.dto import AnalysisContext, AnalysisResult

class BollingerAnalysis(BaseAnalysis):
    def execute(self, context: AnalysisContext) -> AnalysisResult:
        indicator_engine = context.dependencies.get("indicator_engine")
        if not indicator_engine:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": "Indicator Engine unavailable"})
            
        try:
            bb = indicator_engine.get_indicator("BOLLINGER_BANDS", context.market_data)
        except Exception as e:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": str(e)})
            
        if bb is None or len(bb) < 20:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": "Insufficient indicator data"})
            
        # Assuming bb is DataFrame with 'upper', 'middle', 'lower', 'bandwidth'
        curr_bw = bb['bandwidth'].iloc[-1]
        bw_sma = bb['bandwidth'].rolling(window=20).mean().iloc[-1]
        
        classification = "volatility state: stable"
        score = 0.0
        confidence = 0.70
        risk_flags = ["Medium"]
        evidence = [f"BB Bandwidth: {curr_bw:.2f}", f"BB Bandwidth SMA(20): {bw_sma:.2f}"]
        contradictions = []
        
        if curr_bw > bw_sma * 1.2:
            classification = "expansion"
            score = 0.60
            evidence.append("Bandwidth is expanding significantly above average.")
            risk_flags = ["High"]
        elif curr_bw < bw_sma * 0.8:
            classification = "squeeze"
            score = -0.60 # squeeze means low volatility, potential for breakout (but score represents current vol magnitude)
            evidence.append("Bandwidth is in a squeeze (very low volatility).")
            risk_flags = ["Low"]

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
                "metadata": {"dashboard_widget": "band_chart"}
            }
        )
