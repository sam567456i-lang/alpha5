import os
import yaml

EXTREMUM_DIR = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid\Backend\platforms\analysis\extremum"
REGISTRY_PATH = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid\Governance\registry\master_capability_registry.yaml"

os.makedirs(EXTREMUM_DIR, exist_ok=True)

# 1. Register Capabilities
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
            "family": "Extremum",
            "subfamily": subfam,
            "dependencies": [dep]
        })
        print(f"Registered {cid}")

register("ANALYSIS_EXTREMUM_DONCHIAN", "Donchian Channels Analysis", "Donchian", "INDICATOR_DONCHIAN")
register("ANALYSIS_EXTREMUM_HIGHLOW", "High Low Analysis", "HighLow", "INDICATOR_HIGHLOW")
register("ANALYSIS_EXTREMUM_SR", "Support Resistance Analysis", "SupportResistance", "INDICATOR_SR")

with open(REGISTRY_PATH, "w") as f:
    yaml.dump(registry, f, sort_keys=False)

# 2. Write Donchian Analysis
donchian_code = """import pandas as pd
from typing import Dict, Any
from Backend.platforms.analysis.factory.factory import BaseAnalysis
from Backend.platforms.analysis.core.dto import AnalysisContext, AnalysisResult

class DonchianAnalysis(BaseAnalysis):
    def execute(self, context: AnalysisContext) -> AnalysisResult:
        indicator_engine = context.dependencies.get("indicator_engine")
        if not indicator_engine:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": "Indicator Engine unavailable"})
            
        try:
            dc = indicator_engine.get_indicator("DONCHIAN", context.market_data)
        except Exception as e:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": str(e)})
            
        if dc is None or len(dc) < 20:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": "Insufficient indicator data"})
            
        # Assuming dc is DataFrame with 'upper', 'lower', 'middle'
        curr_price = context.market_data['close'].iloc[-1]
        upper = dc['upper'].iloc[-1]
        lower = dc['lower'].iloc[-1]
        
        dist_res = upper - curr_price
        dist_sup = curr_price - lower
        
        classification = "channel position: neutral"
        score = 0.0
        confidence = 0.60
        risk_flags = ["Medium"]
        evidence = [f"Distance to resistance: {dist_res:.2f}", f"Distance to support: {dist_sup:.2f}"]
        contradictions = []
        
        if curr_price >= upper * 0.99:
            classification = "breakout pressure: high (resistance)"
            score = 0.70
            risk_flags = ["High"]
            evidence.append("Price is testing upper Donchian channel.")
        elif curr_price <= lower * 1.01:
            classification = "breakout pressure: high (support)"
            score = -0.70
            risk_flags = ["High"]
            evidence.append("Price is testing lower Donchian channel.")

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
                "metadata": {"dashboard_widget": "channel_chart"}
            }
        )
"""

# 3. Write HighLow Analysis
highlow_code = """import pandas as pd
from typing import Dict, Any
from Backend.platforms.analysis.factory.factory import BaseAnalysis
from Backend.platforms.analysis.core.dto import AnalysisContext, AnalysisResult

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
"""

# 4. Write SupportResistance Analysis
sr_code = """import pandas as pd
from typing import Dict, Any
from Backend.platforms.analysis.factory.factory import BaseAnalysis
from Backend.platforms.analysis.core.dto import AnalysisContext, AnalysisResult

class SupportResistanceAnalysis(BaseAnalysis):
    def execute(self, context: AnalysisContext) -> AnalysisResult:
        indicator_engine = context.dependencies.get("indicator_engine")
        if not indicator_engine:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": "Indicator Engine unavailable"})
            
        try:
            sr = indicator_engine.get_indicator("SR", context.market_data)
        except Exception as e:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": str(e)})
            
        if sr is None or len(sr) == 0:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": "Insufficient indicator data"})
            
        # Assuming sr returns a dict or dataframe of closest S/R levels
        curr_price = context.market_data['close'].iloc[-1]
        resistance = sr['resistance'].iloc[-1]
        support = sr['support'].iloc[-1]
        
        dist_res = resistance - curr_price
        dist_sup = curr_price - support
        
        classification = "channel position: floating"
        score = 0.0
        confidence = 0.75
        risk_flags = ["Medium"]
        evidence = [f"Distance to resistance: {dist_res:.2f}", f"Distance to support: {dist_sup:.2f}"]
        contradictions = []
        
        # If very close to resistance, breakout pressure is high
        if dist_res < (curr_price * 0.01):
            classification = "breakout pressure: critical resistance"
            score = 0.80
            risk_flags = ["High"]
            evidence.append("Price is within 1% of major resistance.")
        elif dist_sup < (curr_price * 0.01):
            classification = "breakout pressure: critical support"
            score = -0.80
            risk_flags = ["High"]
            evidence.append("Price is within 1% of major support.")

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
                "metadata": {"dashboard_widget": "levels_chart"}
            }
        )
"""

with open(os.path.join(EXTREMUM_DIR, "donchian_analysis.py"), "w") as f:
    f.write(donchian_code)
with open(os.path.join(EXTREMUM_DIR, "highlow_analysis.py"), "w") as f:
    f.write(highlow_code)
with open(os.path.join(EXTREMUM_DIR, "sr_analysis.py"), "w") as f:
    f.write(sr_code)

print("Project OS Audit: Extremum dependencies mapped. Generated Donchian, HighLow, and SR Analyses.")
