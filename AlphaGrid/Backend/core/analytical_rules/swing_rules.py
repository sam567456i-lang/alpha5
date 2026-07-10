from typing import Dict, Any, Optional
from Backend.core.evidence_dtos.swing import (
    PivotEvidence,
    PivotLifecycleEvidence,
    SwingClassificationEvidence,
    SwingRelationshipEvidence,
    SwingQualityEvidence
)

class SwingRelationshipRule:
    """Computes relationship between two pivots."""
    
    def evaluate(self, current_pivot: PivotEvidence, previous_pivot: PivotEvidence, atr: float, tolerance: float = 0.1, tick_size: float = 0.01, n_ticks: int = 5) -> SwingRelationshipEvidence:
        price_c = current_pivot.price
        price_p = previous_pivot.price
        
        # Absolute threshold for equality: max(Tolerance * ATR, TickSize * n)
        threshold = max(atr * tolerance, tick_size * n_ticks)
        
        # Determine Relationship
        if current_pivot.pivot_type == "High" and previous_pivot.pivot_type == "High":
            if abs(price_c - price_p) <= threshold:
                rel = "EQH"
            elif abs(price_c - price_p) <= threshold * 2:
                rel = "NEQH"
            elif price_c > price_p + threshold:
                rel = "HH"
            else:
                rel = "LH"
        elif current_pivot.pivot_type == "Low" and previous_pivot.pivot_type == "Low":
            if abs(price_c - price_p) <= threshold:
                rel = "EQL"
            elif abs(price_c - price_p) <= threshold * 2:
                rel = "NEQL"
            elif price_c < price_p - threshold:
                rel = "LL"
            else:
                rel = "HL"
        else:
            # comparing high to low, rarely done directly in HH/LL terms but might be needed for magnitude
            rel = "NONE"
            
        return SwingRelationshipEvidence(
            asset=current_pivot.asset,
            timeframe=current_pivot.timeframe,
            timestamp=current_pivot.timestamp,
            relationship=rel,
            origin_pivot_timestamp=previous_pivot.timestamp,
            current_pivot_timestamp=current_pivot.timestamp
        )

class SwingQualityRule:
    """Computes objective quality metrics for a swing."""
    
    def evaluate(self, start_pivot: PivotEvidence, end_pivot: PivotEvidence, atr: float, volume_sum: float = 0.0) -> SwingQualityEvidence:
        magnitude = abs(end_pivot.price - start_pivot.price)
        duration = end_pivot.timestamp - start_pivot.timestamp
        
        # A simple volatility-adjusted significance
        vol_adj = magnitude / atr if atr > 0 else 0.0
        
        return SwingQualityEvidence(
            asset=end_pivot.asset,
            timeframe=end_pivot.timeframe,
            timestamp=end_pivot.timestamp,
            magnitude=magnitude,
            duration=duration,
            symmetry_ratio=1.0, # Will be updated with sub-swings in full engine
            volatility_adjusted_significance=vol_adj,
            confirmation_bars=0, # Computed by PersistenceEngine
            volume_support=volume_sum
        )
