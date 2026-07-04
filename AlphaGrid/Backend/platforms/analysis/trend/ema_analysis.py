import pandas as pd
from typing import Dict, Any
from Backend.platforms.analysis.factory.factory import BaseAnalysis
from Backend.platforms.analysis.core.dto import AnalysisContext, AnalysisResult

class EMAAnalysis(BaseAnalysis):
    def execute(self, context: AnalysisContext) -> AnalysisResult:
        indicator_engine = context.dependencies.get("indicator_engine")
        
        # Strict Enforcement: No Pandas-TA fallback.
        if not indicator_engine:
            return AnalysisResult(
                score=0.0,
                raw_data=context.market_data,
                metadata={
                    "status": "Unsupported",
                    "reason": "Required Indicator Engine unavailable"
                }
            )
            
        try:
            # Consume Indicator Engine for EMA values
            ema_20 = indicator_engine.get_indicator("EMA", context.market_data, length=20)
            ema_50 = indicator_engine.get_indicator("EMA", context.market_data, length=50)
            ema_200 = indicator_engine.get_indicator("EMA", context.market_data, length=200)
        except Exception as e:
            return AnalysisResult(
                score=0.0,
                raw_data=context.market_data,
                metadata={
                    "status": "Unsupported",
                    "reason": f"Required indicators unavailable: {str(e)}"
                }
            )
            
        # Get the latest values
        if ema_20.empty or ema_50.empty or ema_200.empty:
            return AnalysisResult(
                score=0.0,
                raw_data=context.market_data,
                metadata={"status": "Unsupported", "reason": "Empty indicator data"}
            )
            
        latest_20 = ema_20.iloc[-1]
        latest_50 = ema_50.iloc[-1]
        latest_200 = ema_200.iloc[-1]
        latest_price = context.market_data['close'].iloc[-1]
        
        # Determine Market State (What does the market look like?)
        trend_state = "Neutral"
        score = 0.0
        confidence = 0.0
        risk = "Medium"
        evidence = f"EMA20: {latest_20:.2f}, EMA50: {latest_50:.2f}, EMA200: {latest_200:.2f}"
        contradictions = "None"
        
        if latest_20 > latest_50 > latest_200:
            if latest_price > latest_20:
                trend_state = "Strong Uptrend"
                score = 0.85
                confidence = 0.90
                risk = "Low"
                evidence = "Price > EMA20 > EMA50 > EMA200. Perfect bullish alignment."
            else:
                trend_state = "Weakening Uptrend"
                score = 0.50
                confidence = 0.60
                risk = "High"
                evidence = "EMA20 > EMA50 > EMA200, but Price fell below EMA20."
                contradictions = "Price momentum decoupling from moving averages."
                
        elif latest_20 < latest_50 < latest_200:
            if latest_price < latest_20:
                trend_state = "Strong Downtrend"
                score = -0.85
                confidence = 0.90
                risk = "Low"
                evidence = "Price < EMA20 < EMA50 < EMA200. Perfect bearish alignment."
            else:
                trend_state = "Weakening Downtrend"
                score = -0.50
                confidence = 0.60
                risk = "High"
                evidence = "EMA20 < EMA50 < EMA200, but Price broke above EMA20."
                contradictions = "Price momentum attempting bullish reversal against moving averages."
        else:
            trend_state = "Chop / Range"
            score = 0.0
            confidence = 0.30
            risk = "High"
            evidence = "Moving averages are crossed/tangled."

        return AnalysisResult(
            score=score,
            raw_data=context.market_data,
            signals=[],  # Explicitly empty. No Buy/Sell generated.
            metadata={
                "status": "Success",
                "trend": trend_state,
                "confidence": confidence,
                "evidence": evidence,
                "risk": risk,
                "contradictions": contradictions,
                "quality": "High"
            }
        )
