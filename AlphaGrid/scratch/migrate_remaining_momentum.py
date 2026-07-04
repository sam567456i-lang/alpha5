import os
import yaml

MOMENTUM_DIR = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid\Backend\platforms\analysis\momentum"
REGISTRY_PATH = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid\Governance\registry\master_capability_registry.yaml"

# 1. Register Composite Momentum
with open(REGISTRY_PATH, "r") as f:
    registry = yaml.safe_load(f) or {"capabilities": []}
caps = registry.setdefault("capabilities", [])
exists = any(c.get("capability_id") == "ANALYSIS_MOMENTUM_COMPOSITE" for c in caps)
if not exists:
    caps.append({
        "capability_id": "ANALYSIS_MOMENTUM_COMPOSITE",
        "name": "Composite Momentum Analysis",
        "platform": "P05_Analysis",
        "family": "Momentum",
        "subfamily": "Composite",
        "dependencies": ["INDICATOR_RSI", "INDICATOR_MACD"]
    })
    with open(REGISTRY_PATH, "w") as f:
        yaml.dump(registry, f, sort_keys=False)

# 2. Write MACD Analysis
macd_code = """import pandas as pd
from typing import Dict, Any
from Backend.platforms.analysis.factory.factory import BaseAnalysis
from Backend.platforms.analysis.core.dto import AnalysisContext, AnalysisResult

class MACDAnalysis(BaseAnalysis):
    def execute(self, context: AnalysisContext) -> AnalysisResult:
        indicator_engine = context.dependencies.get("indicator_engine")
        if not indicator_engine:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": "Indicator Engine unavailable"})
            
        try:
            macd = indicator_engine.get_indicator("MACD", context.market_data)
        except Exception as e:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": str(e)})
            
        if macd is None or len(macd) < 2:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": "Empty indicator data"})
            
        # Assuming MACD returns a DataFrame with 'macd', 'signal', 'hist'
        curr_macd = macd['macd'].iloc[-1]
        curr_signal = macd['signal'].iloc[-1]
        curr_hist = macd['hist'].iloc[-1]
        prev_hist = macd['hist'].iloc[-2]
        
        classification = "Neutral"
        score = 0.0
        confidence = 0.50
        risk_flags = ["Medium"]
        evidence = [f"MACD: {curr_macd:.2f}", f"Signal: {curr_signal:.2f}", f"Hist: {curr_hist:.2f}"]
        contradictions = []
        
        if curr_macd > curr_signal:
            if curr_hist > prev_hist:
                classification = "Strong Bullish Momentum"
                score = 0.80
                confidence = 0.85
                risk_flags = ["Low"]
                evidence.append("MACD is above Signal and Histogram is expanding.")
            else:
                classification = "Weakening Bullish Momentum"
                score = 0.40
                confidence = 0.60
                risk_flags = ["Medium"]
                evidence.append("MACD is above Signal but Histogram is shrinking.")
        elif curr_macd < curr_signal:
            if curr_hist < prev_hist:
                classification = "Strong Bearish Momentum"
                score = -0.80
                confidence = 0.85
                risk_flags = ["Low"]
                evidence.append("MACD is below Signal and Histogram is expanding negatively.")
            else:
                classification = "Weakening Bearish Momentum"
                score = -0.40
                confidence = 0.60
                risk_flags = ["Medium"]
                evidence.append("MACD is below Signal but Histogram is shrinking.")

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
                "metadata": {"dashboard_widget": "macd_histogram"}
            }
        )
"""

# 3. Write Composite Momentum Analysis
composite_code = """import pandas as pd
from typing import Dict, Any
from Backend.platforms.analysis.factory.factory import BaseAnalysis
from Backend.platforms.analysis.core.dto import AnalysisContext, AnalysisResult
from Backend.platforms.analysis.momentum.rsi_analysis import RSIAnalysis
from Backend.platforms.analysis.momentum.macd_analysis import MACDAnalysis

class CompositeMomentumAnalysis(BaseAnalysis):
    def execute(self, context: AnalysisContext) -> AnalysisResult:
        # Executes sub-analyses directly.
        rsi_analyzer = RSIAnalysis()
        macd_analyzer = MACDAnalysis()
        
        rsi_result = rsi_analyzer.execute(context)
        macd_result = macd_analyzer.execute(context)
        
        if rsi_result.metadata.get("status") == "Unsupported" or macd_result.metadata.get("status") == "Unsupported":
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": "Sub-analyzers unavailable"})
            
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
"""

with open(os.path.join(MOMENTUM_DIR, "macd_analysis.py"), "w") as f:
    f.write(macd_code)

with open(os.path.join(MOMENTUM_DIR, "composite_momentum_analysis.py"), "w") as f:
    f.write(composite_code)

print("Generated MACD and Composite Momentum classes.")
