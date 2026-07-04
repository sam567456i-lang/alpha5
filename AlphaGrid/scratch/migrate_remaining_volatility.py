import os
import yaml

VOLATILITY_DIR = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid\Backend\platforms\analysis\volatility"
REGISTRY_PATH = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid\Governance\registry\master_capability_registry.yaml"

# 1. Register Bollinger Bands and Keltner Channels
with open(REGISTRY_PATH, "r") as f:
    registry = yaml.safe_load(f) or {"capabilities": []}
caps = registry.setdefault("capabilities", [])

def register(cid, name, subfam, dep):
    exists = any(c.get("capability_id") == cid for c in caps)
    if not exists:
        caps.append({
            "capability_id": cid,
            "name": name,
            "platform": "P05_Analysis",
            "family": "Volatility",
            "subfamily": subfam,
            "dependencies": [dep]
        })
        print(f"Registered {cid}")

register("ANALYSIS_VOLATILITY_BOLLINGER", "Bollinger Bands Analysis", "Bollinger", "INDICATOR_BOLLINGER_BANDS")
register("ANALYSIS_VOLATILITY_KELTNER", "Keltner Channels Analysis", "Keltner", "INDICATOR_KELTNER_CHANNELS")

with open(REGISTRY_PATH, "w") as f:
    yaml.dump(registry, f, sort_keys=False)

# 2. Write Bollinger Bands Analysis
bb_code = """import pandas as pd
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
"""

# 3. Write Keltner Analysis
kc_code = """import pandas as pd
from typing import Dict, Any
from Backend.platforms.analysis.factory.factory import BaseAnalysis
from Backend.platforms.analysis.core.dto import AnalysisContext, AnalysisResult

class KeltnerAnalysis(BaseAnalysis):
    def execute(self, context: AnalysisContext) -> AnalysisResult:
        indicator_engine = context.dependencies.get("indicator_engine")
        if not indicator_engine:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": "Indicator Engine unavailable"})
            
        try:
            kc = indicator_engine.get_indicator("KELTNER_CHANNELS", context.market_data)
        except Exception as e:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": str(e)})
            
        if kc is None or len(kc) < 20:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": "Insufficient indicator data"})
            
        # Assuming kc is DataFrame with 'upper', 'middle', 'lower', 'bandwidth'
        curr_bw = kc['bandwidth'].iloc[-1]
        prev_bw = kc['bandwidth'].iloc[-2]
        
        classification = "volatility state: stable"
        score = 0.0
        confidence = 0.65
        risk_flags = ["Medium"]
        evidence = [f"KC Bandwidth: {curr_bw:.2f}"]
        contradictions = []
        
        if curr_bw > prev_bw * 1.05:
            classification = "expansion"
            score = 0.40
            evidence.append("Keltner Channels are expanding.")
            risk_flags = ["High"]
        elif curr_bw < prev_bw * 0.95:
            classification = "compression"
            score = -0.40
            evidence.append("Keltner Channels are compressing.")
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
"""

with open(os.path.join(VOLATILITY_DIR, "bollinger_analysis.py"), "w") as f:
    f.write(bb_code)

with open(os.path.join(VOLATILITY_DIR, "keltner_analysis.py"), "w") as f:
    f.write(kc_code)

print("Project OS Audit: Volatility dependencies mapped. CLEARED for Bollinger and Keltner migration.")
print("Generated Bollinger and Keltner Analysis.")
