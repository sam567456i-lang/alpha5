import os
import yaml

VOLUME_DIR = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid\Backend\platforms\analysis\volume"
REGISTRY_PATH = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid\Governance\registry\master_capability_registry.yaml"

os.makedirs(VOLUME_DIR, exist_ok=True)

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
            "family": "Volume",
            "subfamily": subfam,
            "dependencies": [dep]
        })
        print(f"Registered {cid}")

register("ANALYSIS_VOLUME_VWAP", "VWAP Analysis", "VWAP", "INDICATOR_VWAP")
register("ANALYSIS_VOLUME_OBV", "OBV Analysis", "OBV", "INDICATOR_OBV")
register("ANALYSIS_VOLUME_SMA", "Volume SMA Analysis", "VolumeSMA", "INDICATOR_VOLUME_SMA")
register("ANALYSIS_VOLUME_AD", "Accumulation Distribution Analysis", "AccDist", "INDICATOR_ACC_DIST")

with open(REGISTRY_PATH, "w") as f:
    yaml.dump(registry, f, sort_keys=False)

# 2. Write VWAP Analysis
vwap_code = """import pandas as pd
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
"""

# 3. Write OBV Analysis
obv_code = """import pandas as pd
from typing import Dict, Any
from Backend.platforms.analysis.factory.factory import BaseAnalysis
from Backend.platforms.analysis.core.dto import AnalysisContext, AnalysisResult

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
"""

# 4. Write Volume SMA Analysis
vsma_code = """import pandas as pd
from typing import Dict, Any
from Backend.platforms.analysis.factory.factory import BaseAnalysis
from Backend.platforms.analysis.core.dto import AnalysisContext, AnalysisResult

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
"""

# 5. Write Accumulation/Distribution Analysis
ad_code = """import pandas as pd
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
"""

with open(os.path.join(VOLUME_DIR, "vwap_analysis.py"), "w") as f:
    f.write(vwap_code)
with open(os.path.join(VOLUME_DIR, "obv_analysis.py"), "w") as f:
    f.write(obv_code)
with open(os.path.join(VOLUME_DIR, "volume_sma_analysis.py"), "w") as f:
    f.write(vsma_code)
with open(os.path.join(VOLUME_DIR, "ad_analysis.py"), "w") as f:
    f.write(ad_code)

print("Project OS Audit: Volume dependencies mapped. Generated VWAP, OBV, Volume SMA, and A/D Analyses.")
