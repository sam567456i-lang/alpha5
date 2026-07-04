import pandas as pd
from typing import Dict, Any
from Backend.platforms.analysis.factory.factory import BaseAnalysis
from Backend.platforms.analysis.core.dto import AnalysisContext, AnalysisResult

class SMAAnalysis(BaseAnalysis):
    def execute(self, context: AnalysisContext) -> AnalysisResult:
        indicator_engine = context.dependencies.get("indicator_engine")
        
        if not indicator_engine:
            return AnalysisResult(
                score=0.0,
                raw_data=context.market_data,
                metadata={"status": "Unsupported", "reason": "Required Indicator Engine unavailable"}
            )
            
        try:
            sma_20 = indicator_engine.get_indicator("SMA", context.market_data, length=20)
            sma_50 = indicator_engine.get_indicator("SMA", context.market_data, length=50)
            sma_200 = indicator_engine.get_indicator("SMA", context.market_data, length=200)
        except Exception as e:
            return AnalysisResult(
                score=0.0,
                raw_data=context.market_data,
                metadata={"status": "Unsupported", "reason": f"Required indicators unavailable: {str(e)}"}
            )
            
        if sma_20.empty or sma_50.empty or sma_200.empty:
            return AnalysisResult(
                score=0.0,
                raw_data=context.market_data,
                metadata={"status": "Unsupported", "reason": "Empty indicator data"}
            )
            
        latest_20 = sma_20.iloc[-1]
        latest_50 = sma_50.iloc[-1]
        latest_200 = sma_200.iloc[-1]
        latest_price = context.market_data['close'].iloc[-1]
        
        trend_state = "Neutral"
        score = 0.0
        confidence = 0.0
        risk = "Medium"
        evidence = f"SMA20: {latest_20:.2f}, SMA50: {latest_50:.2f}, SMA200: {latest_200:.2f}"
        contradictions = "None"
        
        if latest_20 > latest_50 > latest_200:
            if latest_price > latest_20:
                trend_state = "Strong Uptrend"
                score = 0.80
                confidence = 0.85
                risk = "Low"
                evidence = "Price > SMA20 > SMA50 > SMA200. Bullish alignment."
            else:
                trend_state = "Weakening Uptrend"
                score = 0.40
                confidence = 0.50
                risk = "High"
                evidence = "SMA20 > SMA50 > SMA200, but Price fell below SMA20."
                contradictions = "Price falling against long-term trend."
                
        elif latest_20 < latest_50 < latest_200:
            if latest_price < latest_20:
                trend_state = "Strong Downtrend"
                score = -0.80
                confidence = 0.85
                risk = "Low"
                evidence = "Price < SMA20 < SMA50 < SMA200. Bearish alignment."
            else:
                trend_state = "Weakening Downtrend"
                score = -0.40
                confidence = 0.50
                risk = "High"
                evidence = "SMA20 < SMA50 < SMA200, but Price broke above SMA20."
                contradictions = "Price rising against long-term downtrend."
        else:
            trend_state = "Chop / Range"
            score = 0.0
            confidence = 0.20
            risk = "High"
            evidence = "Simple moving averages are tangled."

        return AnalysisResult(
            score=score,
            raw_data=context.market_data,
            signals=[],
            metadata={
                "status": "Success",
                "trend": trend_state,
                "confidence": confidence,
                "evidence": evidence,
                "risk": risk,
                "contradictions": contradictions,
                "quality": "Medium" # SMA is laggy, quality is medium compared to EMA
            }
        )
