"""
Exchange Contracts.

Defines the base interface for market exchanges and provides
a concrete implementation for the National Stock Exchange of India (NSE).

Dependency Graph:
    Consumes: []
    Produces: [ExchangeContract, NSEImplementation]
    Registry: MarketIntelligenceRegistry (Future)
    Downstream: TradingCalendar, SessionEngine
    Owner: MarketIntelligenceTeam
"""

import abc
from typing import List, Dict
from datetime import time, timedelta

class ExchangeContract(abc.ABC):
    """Base interface for all market exchanges."""

    @property
    @abc.abstractmethod
    def exchange_code(self) -> str:
        """Returns the canonical code (e.g., 'NSE', 'BSE')."""
        pass

    @property
    @abc.abstractmethod
    def timezone(self) -> str:
        """Returns the IANA timezone string (e.g., 'Asia/Kolkata')."""
        pass

    @abc.abstractmethod
    def get_standard_market_hours(self) -> Dict[str, time]:
        """
        Returns standard market open and close times.
        Expected keys: 'pre_open', 'open', 'close', 'post_close'
        """
        pass


class NSEImplementation(ExchangeContract):
    """Concrete implementation for the National Stock Exchange of India (NSE)."""

    @property
    def exchange_code(self) -> str:
        return "NSE"

    @property
    def timezone(self) -> str:
        return "Asia/Kolkata"

    def get_standard_market_hours(self) -> Dict[str, time]:
        """
        Standard NSE Market Hours.
        Pre-open: 09:00 - 09:15
        Open: 09:15 - 15:30
        Post-close: 15:30 - 16:00
        """
        return {
            "pre_open_start": time(9, 0),
            "pre_open_end": time(9, 15),
            "open": time(9, 15),
            "close": time(15, 30),
            "post_close_end": time(16, 0)
        }
