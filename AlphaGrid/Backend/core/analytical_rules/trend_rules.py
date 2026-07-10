from typing import Dict, Any
from Backend.core.evidence_dtos.trend import (
    TrendDirectionEvidence,
    TrendStrengthEvidence,
    TrendSlopeEvidence,
    TrendStateEvidence
)

class TrendDirectionRule:
    """Classifies slope into objective direction."""
    
    def evaluate(self, slope: float, threshold: float, meta: Dict[str, Any]) -> TrendDirectionEvidence:
        if slope > threshold:
            direction = "Up"
        elif slope < -threshold:
            direction = "Down"
        else:
            direction = "Neutral"
            
        return TrendDirectionEvidence(
            asset=meta.get("asset", "UNKNOWN"),
            timeframe=meta.get("timeframe", "1m"),
            timestamp=meta.get("timestamp", 0),
            direction=direction,
            raw_slope=slope
        )

class TrendStrengthRule:
    """Classifies raw strength scores based on configurable thresholds."""
    
    def evaluate(self, raw_score: float, weak_thresh: float, strong_thresh: float, meta: Dict[str, Any]) -> TrendStrengthEvidence:
        if raw_score < weak_thresh:
            classification = "Weak"
        elif raw_score >= strong_thresh:
            classification = "Strong"
        else:
            classification = "Moderate"
            
        return TrendStrengthEvidence(
            asset=meta.get("asset", "UNKNOWN"),
            timeframe=meta.get("timeframe", "1m"),
            timestamp=meta.get("timestamp", 0),
            strength_classification=classification,
            raw_strength_score=raw_score
        )

class TrendStateRule:
    """Detects objective structural state based on geometry and volatility."""
    
    def evaluate(self, 
                 direction: str, 
                 strength: str, 
                 accel: float, 
                 slope: float, 
                 volatility_regime: str,
                 meta: Dict[str, Any]) -> TrendStateEvidence:
                 
        state = "Consolidation"
        
        if direction != meta.get("prev_direction", direction):
            state = "Transition"
        elif volatility_regime == "Expanding":
            state = "Expansion"
        elif volatility_regime == "Contracting":
            state = "Compression"
        elif strength == "Strong":
            # If accelerating in direction of slope, it's impulse
            if (accel > 0 and slope > 0) or (accel < 0 and slope < 0):
                state = "Impulse"
            else:
                state = "Correction"
                
        return TrendStateEvidence(
            asset=meta.get("asset", "UNKNOWN"),
            timeframe=meta.get("timeframe", "1m"),
            timestamp=meta.get("timestamp", 0),
            state=state
        )
