from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod
from Backend.core.evidence_dtos.swing import PivotEvidence

class PivotDetectionPolicy(ABC):
    """Abstract interface for objective pivot detection algorithms."""
    @abstractmethod
    def process(self, history: List[Dict[str, Any]], new_event: Dict[str, Any]) -> Optional[PivotEvidence]:
        pass

class ZigZagPolicy(PivotDetectionPolicy):
    """Placeholder for ZigZag algorithm pivot detection."""
    def process(self, history: List[Dict[str, Any]], new_event: Dict[str, Any]) -> Optional[PivotEvidence]:
        # Pending implementation
        return None

class ATRPivotPolicy(PivotDetectionPolicy):
    """Placeholder for ATR-based adaptive pivot detection."""
    def process(self, history: List[Dict[str, Any]], new_event: Dict[str, Any]) -> Optional[PivotEvidence]:
        # Pending implementation
        return None

class NBarFractalPolicy(PivotDetectionPolicy):
    """Detects pivots using an N-bar window."""
    def __init__(self, n: int = 2):
        self.n = n
        
    def process(self, history: List[Dict[str, Any]], new_event: Dict[str, Any]) -> Optional[PivotEvidence]:
        # Requires at least 2*N + 1 bars
        if len(history) < 2 * self.n + 1:
            return None
            
        # The candidate pivot is at index N (from the right)
        candidate_idx = - (self.n + 1)
        candidate_event = history[candidate_idx]
        
        # Check High
        is_high = True
        is_low = True
        
        c_high = candidate_event.get("high", 0)
        c_low = candidate_event.get("low", 0)
        
        for i in range(- (2 * self.n + 1), 0):
            if i == candidate_idx:
                continue
            if history[i].get("high", 0) >= c_high:
                is_high = False
            if history[i].get("low", float('inf')) <= c_low:
                is_low = False
                
        if is_high:
            return PivotEvidence(
                asset=candidate_event.get("symbol", "UNKNOWN"),
                timeframe=candidate_event.get("timeframe", "1m"),
                timestamp=candidate_event.get("timestamp", 0),
                pivot_type="High",
                price=c_high
            )
        if is_low:
            return PivotEvidence(
                asset=candidate_event.get("symbol", "UNKNOWN"),
                timeframe=candidate_event.get("timeframe", "1m"),
                timestamp=candidate_event.get("timestamp", 0),
                pivot_type="Low",
                price=c_low
            )
            
        return None

class PivotEngine:
    """
    Platform 10: Swing Family - Pivot Engine.
    Executes a pluggable PivotDetectionPolicy.
    """
    def __init__(self, policy: PivotDetectionPolicy):
        self.policy = policy
        self.history = []
        # In a real streaming system, history would be bounded
        self.max_history = 100 
        
    def process_event(self, event: Dict[str, Any]) -> Optional[PivotEvidence]:
        self.history.append(event)
        if len(self.history) > self.max_history:
            self.history.pop(0)
            
        return self.policy.process(self.history, event)

    def name(self) -> str:
        return "PivotEngine"
