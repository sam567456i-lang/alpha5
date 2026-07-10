import math
from typing import List, Dict, Any
from Backend.core.evidence_dtos.statistics import (
    DistributionEvidence,
    VolatilityEvidence,
    NormalizationEvidence
)

class DistributionRule:
    """Computes mean, variance, skewness, kurtosis for a window of data."""
    
    def evaluate(self, market_data: Dict[str, Any]) -> DistributionEvidence:
        closes: List[float] = market_data.get("closes", [])
        if not closes:
            return None
            
        n = len(closes)
        mean = sum(closes) / n
        
        if n < 2:
            return DistributionEvidence(
                asset=market_data.get("asset", "UNKNOWN"),
                timeframe=market_data.get("timeframe", "1m"),
                timestamp=market_data.get("timestamp", 0),
                mean=mean, variance=0.0, skewness=0.0, kurtosis=0.0, entropy=0.0
            )
            
        variance = sum((x - mean) ** 2 for x in closes) / (n - 1)
        std_dev = math.sqrt(variance)
        
        # simplified skewness & kurtosis for objective measurement
        skewness = 0.0
        kurtosis = 0.0
        if std_dev > 1e-8:
            skewness = (sum((x - mean) ** 3 for x in closes) / n) / (std_dev ** 3)
            kurtosis = (sum((x - mean) ** 4 for x in closes) / n) / (std_dev ** 4)
            
        return DistributionEvidence(
            asset=market_data.get("asset", "UNKNOWN"),
            timeframe=market_data.get("timeframe", "1m"),
            timestamp=market_data.get("timestamp", 0),
            mean=mean,
            variance=variance,
            skewness=skewness,
            kurtosis=kurtosis,
            entropy=0.0  # Placeholder for Shannon entropy computation
        )


class VolatilityRule:
    """Computes ATR, Parkinson, and True Range objectively."""
    
    def evaluate(self, market_data: Dict[str, Any]) -> VolatilityEvidence:
        high = market_data.get("high", 0.0)
        low = market_data.get("low", 0.0)
        prev_close = market_data.get("prev_close", 0.0)
        
        tr = max(high - low, abs(high - prev_close), abs(low - prev_close))
        
        # In a real streaming engine, ATR is updated iteratively.
        # This rule demonstrates the objective calculation mapping.
        current_atr = market_data.get("current_atr", tr)
        
        # Parkinson Volatility: sqrt(1/(4*ln(2)) * (ln(H/L))^2)
        parkinson = 0.0
        if low > 0:
            parkinson = math.sqrt( (1.0 / (4.0 * math.log(2))) * (math.log(high/low) ** 2) )
            
        return VolatilityEvidence(
            asset=market_data.get("asset", "UNKNOWN"),
            timeframe=market_data.get("timeframe", "1m"),
            timestamp=market_data.get("timestamp", 0),
            true_range=tr,
            atr=current_atr,
            historical_volatility=0.0,
            parkinson_volatility=parkinson,
            garman_klass_volatility=0.0,
            volatility_regime="Stable"
        )
