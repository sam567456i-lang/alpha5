import os

TREND_DIR = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid\Backend\platforms\analysis\trend"

ema_code = """import pandas as pd
from typing import Dict, Any
from Backend.platforms.analysis.factory.factory import BaseAnalysis
from Backend.platforms.analysis.core.dto import AnalysisContext, AnalysisResult

class EMAAnalysis(BaseAnalysis):
    def execute(self, context: AnalysisContext) -> AnalysisResult:
        indicator_engine = context.dependencies.get("indicator_engine")
        if not indicator_engine:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": "Indicator Engine unavailable"})
            
        try:
            ema_20 = indicator_engine.get_indicator("EMA", context.market_data, length=20)
            ema_50 = indicator_engine.get_indicator("EMA", context.market_data, length=50)
            ema_200 = indicator_engine.get_indicator("EMA", context.market_data, length=200)
        except Exception as e:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": str(e)})
            
        if ema_20.empty or ema_50.empty or ema_200.empty:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": "Empty indicator data"})
            
        latest_20 = ema_20.iloc[-1]
        latest_50 = ema_50.iloc[-1]
        latest_200 = ema_200.iloc[-1]
        latest_price = context.market_data['close'].iloc[-1]
        
        classification = "Neutral"
        score = 0.0
        confidence = 0.0
        risk_flags = ["Medium"]
        evidence = [f"EMA20: {latest_20:.2f}", f"EMA50: {latest_50:.2f}", f"EMA200: {latest_200:.2f}"]
        contradictions = []
        
        if latest_20 > latest_50 > latest_200:
            if latest_price > latest_20:
                classification = "Strong Uptrend"
                score = 0.85
                confidence = 0.90
                risk_flags = ["Low"]
                evidence.append("Price > EMA20 > EMA50 > EMA200. Perfect bullish alignment.")
            else:
                classification = "Weakening Uptrend"
                score = 0.50
                confidence = 0.60
                risk_flags = ["High"]
                evidence.append("EMA20 > EMA50 > EMA200")
                contradictions.append("Price fell below EMA20.")
                
        elif latest_20 < latest_50 < latest_200:
            if latest_price < latest_20:
                classification = "Strong Downtrend"
                score = -0.85
                confidence = 0.90
                risk_flags = ["Low"]
                evidence.append("Price < EMA20 < EMA50 < EMA200. Perfect bearish alignment.")
            else:
                classification = "Weakening Downtrend"
                score = -0.50
                confidence = 0.60
                risk_flags = ["High"]
                evidence.append("EMA20 < EMA50 < EMA200")
                contradictions.append("Price broke above EMA20.")
        else:
            classification = "Chop / Range"
            score = 0.0
            confidence = 0.30
            risk_flags = ["High"]
            evidence.append("Moving averages are crossed/tangled.")

        return AnalysisResult(
            score=score,
            raw_data=context.market_data,
            signals=[],
            metadata={
                "analysis_type": "trend",
                "status": "completed",
                "overall_score": score,
                "confidence": confidence,
                "classification": classification,
                "evidence": evidence,
                "contradictions": contradictions,
                "risk_flags": risk_flags,
                "quality": "High",
                "metadata": {"dashboard_widget": "trend_ribbon"}
            }
        )
"""

sma_code = """import pandas as pd
from typing import Dict, Any
from Backend.platforms.analysis.factory.factory import BaseAnalysis
from Backend.platforms.analysis.core.dto import AnalysisContext, AnalysisResult

class SMAAnalysis(BaseAnalysis):
    def execute(self, context: AnalysisContext) -> AnalysisResult:
        indicator_engine = context.dependencies.get("indicator_engine")
        if not indicator_engine:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": "Indicator Engine unavailable"})
            
        try:
            sma_20 = indicator_engine.get_indicator("SMA", context.market_data, length=20)
            sma_50 = indicator_engine.get_indicator("SMA", context.market_data, length=50)
            sma_200 = indicator_engine.get_indicator("SMA", context.market_data, length=200)
        except Exception as e:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": str(e)})
            
        if sma_20.empty or sma_50.empty or sma_200.empty:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": "Empty indicator data"})
            
        latest_20 = sma_20.iloc[-1]
        latest_50 = sma_50.iloc[-1]
        latest_200 = sma_200.iloc[-1]
        latest_price = context.market_data['close'].iloc[-1]
        
        classification = "Neutral"
        score = 0.0
        confidence = 0.0
        risk_flags = ["Medium"]
        evidence = [f"SMA20: {latest_20:.2f}", f"SMA50: {latest_50:.2f}", f"SMA200: {latest_200:.2f}"]
        contradictions = []
        
        if latest_20 > latest_50 > latest_200:
            if latest_price > latest_20:
                classification = "Strong Uptrend"
                score = 0.80
                confidence = 0.85
                risk_flags = ["Low"]
                evidence.append("Bullish alignment.")
            else:
                classification = "Weakening Uptrend"
                score = 0.40
                confidence = 0.50
                risk_flags = ["High"]
                contradictions.append("Price fell below SMA20.")
                
        elif latest_20 < latest_50 < latest_200:
            if latest_price < latest_20:
                classification = "Strong Downtrend"
                score = -0.80
                confidence = 0.85
                risk_flags = ["Low"]
                evidence.append("Bearish alignment.")
            else:
                classification = "Weakening Downtrend"
                score = -0.40
                confidence = 0.50
                risk_flags = ["High"]
                contradictions.append("Price broke above SMA20.")
        else:
            classification = "Chop / Range"
            score = 0.0
            confidence = 0.20
            risk_flags = ["High"]
            evidence.append("SMAs are tangled.")

        return AnalysisResult(
            score=score,
            raw_data=context.market_data,
            signals=[],
            metadata={
                "analysis_type": "trend",
                "status": "completed",
                "overall_score": score,
                "confidence": confidence,
                "classification": classification,
                "evidence": evidence,
                "contradictions": contradictions,
                "risk_flags": risk_flags,
                "quality": "Medium",
                "metadata": {}
            }
        )
"""

wma_code = """import pandas as pd
from typing import Dict, Any
from Backend.platforms.analysis.factory.factory import BaseAnalysis
from Backend.platforms.analysis.core.dto import AnalysisContext, AnalysisResult

class WMAAnalysis(BaseAnalysis):
    def execute(self, context: AnalysisContext) -> AnalysisResult:
        indicator_engine = context.dependencies.get("indicator_engine")
        if not indicator_engine:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": "Indicator Engine unavailable"})
            
        try:
            wma_20 = indicator_engine.get_indicator("WMA", context.market_data, length=20)
            wma_50 = indicator_engine.get_indicator("WMA", context.market_data, length=50)
            wma_200 = indicator_engine.get_indicator("WMA", context.market_data, length=200)
        except Exception as e:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": str(e)})
            
        if wma_20.empty or wma_50.empty or wma_200.empty:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": "Empty indicator data"})
            
        latest_20 = wma_20.iloc[-1]
        latest_50 = wma_50.iloc[-1]
        latest_200 = wma_200.iloc[-1]
        
        classification = "Neutral"
        score = 0.0
        confidence = 0.20
        risk_flags = ["Medium"]
        evidence = [f"WMA20: {latest_20:.2f}", f"WMA50: {latest_50:.2f}", f"WMA200: {latest_200:.2f}"]
        
        if latest_20 > latest_50 > latest_200:
            classification = "Strong Uptrend"
            score = 0.85
            confidence = 0.90
            risk_flags = ["Low"]
            evidence.append("Bullish alignment.")
        elif latest_20 < latest_50 < latest_200:
            classification = "Strong Downtrend"
            score = -0.85
            confidence = 0.90
            risk_flags = ["Low"]
            evidence.append("Bearish alignment.")
            
        return AnalysisResult(
            score=score,
            raw_data=context.market_data,
            signals=[],
            metadata={
                "analysis_type": "trend",
                "status": "completed",
                "overall_score": score,
                "confidence": confidence,
                "classification": classification,
                "evidence": evidence,
                "contradictions": [],
                "risk_flags": risk_flags,
                "quality": "High",
                "metadata": {}
            }
        )
"""

macross_code = """import pandas as pd
from typing import Dict, Any
from Backend.platforms.analysis.factory.factory import BaseAnalysis
from Backend.platforms.analysis.core.dto import AnalysisContext, AnalysisResult

class MACrossAnalysis(BaseAnalysis):
    def execute(self, context: AnalysisContext) -> AnalysisResult:
        indicator_engine = context.dependencies.get("indicator_engine")
        if not indicator_engine:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": "Indicator Engine unavailable"})
            
        try:
            sma_50 = indicator_engine.get_indicator("SMA", context.market_data, length=50)
            sma_200 = indicator_engine.get_indicator("SMA", context.market_data, length=200)
        except Exception as e:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": str(e)})
            
        if len(sma_50) < 2 or len(sma_200) < 2:
            return AnalysisResult(0.0, context.market_data, [], {"status": "Unsupported", "reason": "Insufficient data for cross"})
            
        curr_50, prev_50 = sma_50.iloc[-1], sma_50.iloc[-2]
        curr_200, prev_200 = sma_200.iloc[-1], sma_200.iloc[-2]
        
        classification = "Neutral"
        score = 0.0
        confidence = 0.50
        risk_flags = ["Medium"]
        evidence = [f"50SMA: {curr_50:.2f}", f"200SMA: {curr_200:.2f}"]
        
        if prev_50 <= prev_200 and curr_50 > curr_200:
            classification = "Golden Cross (Bullish Reversal)"
            score = 0.90
            confidence = 0.95
            risk_flags = ["Low"]
            evidence.append("50 SMA just crossed ABOVE 200 SMA.")
        elif prev_50 >= prev_200 and curr_50 < curr_200:
            classification = "Death Cross (Bearish Reversal)"
            score = -0.90
            confidence = 0.95
            risk_flags = ["Low"]
            evidence.append("50 SMA just crossed BELOW 200 SMA.")
        elif curr_50 > curr_200:
            classification = "Uptrend"
            score = 0.50
            evidence.append("50 SMA is above 200 SMA (no recent cross).")
        else:
            classification = "Downtrend"
            score = -0.50
            evidence.append("50 SMA is below 200 SMA (no recent cross).")
            
        return AnalysisResult(
            score=score,
            raw_data=context.market_data,
            signals=[],
            metadata={
                "analysis_type": "trend",
                "status": "completed",
                "overall_score": score,
                "confidence": confidence,
                "classification": classification,
                "evidence": evidence,
                "contradictions": [],
                "risk_flags": risk_flags,
                "quality": "Very High",
                "metadata": {}
            }
        )
"""

with open(os.path.join(TREND_DIR, "ema_analysis.py"), "w") as f:
    f.write(ema_code)

with open(os.path.join(TREND_DIR, "sma_analysis.py"), "w") as f:
    f.write(sma_code)

with open(os.path.join(TREND_DIR, "wma_analysis.py"), "w") as f:
    f.write(wma_code)

with open(os.path.join(TREND_DIR, "ma_cross_analysis.py"), "w") as f:
    f.write(macross_code)

print("Refactored all Trend components to use the Generic DTO schema.")
