"""
Event Awareness Engine.

Tracks high-risk events (RBI announcements, Union Budgets, FOMC, Expiries).
Provides awareness of periods where volatility is expected to spike.

Dependency Graph:
    Consumes: [EconomicCalendarProvider]
    Produces: [RiskEventStatus]
    Registry: MarketIntelligenceRegistry (Future)
    Downstream: OpportunityScanner, RiskEngine
    Owner: MarketIntelligenceTeam
"""

from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class RiskEvent:
    name: str
    timestamp: datetime
    impact_level: str # e.g. "HIGH", "MEDIUM", "LOW"
    country: str


class EventAwarenessEngine:
    """Tracks and evaluates upcoming high-risk economic events."""

    def __init__(self, calendar_provider: Any = None):
        """
        Initializes the Event Awareness Engine.
        
        Args:
            calendar_provider: Provider for economic events.
        """
        self._provider = calendar_provider
        self._events: List[RiskEvent] = []

    def load_events(self, events: List[RiskEvent]) -> None:
        """Loads a list of known risk events into the engine."""
        self._events.extend(events)

    def is_high_risk_window(self, timestamp: datetime, window_minutes: int = 60) -> bool:
        """
        Checks if the given timestamp is within a defined window of a HIGH impact event.
        
        Args:
            timestamp (datetime): The time to evaluate.
            window_minutes (int): The number of minutes before/after the event to consider risky.
            
        Returns:
            bool: True if inside a high-risk window, False otherwise.
        """
        for event in self._events:
            if event.impact_level == "HIGH":
                delta = abs((timestamp - event.timestamp).total_seconds())
                if delta <= (window_minutes * 60):
                    return True
        return False
        
    def get_upcoming_events(self, timestamp: datetime, limit: int = 5) -> List[RiskEvent]:
        """
        Returns the next `limit` events strictly after the timestamp.
        """
        upcoming = [e for e in self._events if e.timestamp > timestamp]
        upcoming.sort(key=lambda e: e.timestamp)
        return upcoming[:limit]
