"""
Trading Calendar.

Manages holiday rules, expiry resolution, and exchange calendar integration.
Provides authoritative answers on whether a specific date is a trading day.

Dependency Graph:
    Consumes: [ExchangeContract]
    Produces: [Calendar Events, Holiday States]
    Registry: MarketIntelligenceRegistry (Future)
    Downstream: MarketStateEngine, NormalizationEngine
    Owner: MarketIntelligenceTeam
"""

from datetime import datetime, date
from typing import List, Dict, Any, Optional

class TradingCalendar:
    """Manages trading holidays and expiries."""

    def __init__(self, exchange_contract: Any = None):
        """
        Initializes the Trading Calendar.
        
        Args:
            exchange_contract: The contract defining the exchange details.
        """
        self._exchange = exchange_contract
        self._holidays: set[date] = set()
        self._expiries: Dict[str, set[date]] = {} # e.g. {"NIFTY": {date(2026, 7, 30)}}

    def load_holidays(self, holidays: List[date]) -> None:
        """Loads a list of known holiday dates."""
        self._holidays.update(holidays)

    def load_expiries(self, symbol: str, expiries: List[date]) -> None:
        """Loads expiry dates for a specific symbol."""
        if symbol not in self._expiries:
            self._expiries[symbol] = set()
        self._expiries[symbol].update(expiries)

    def is_holiday(self, timestamp: datetime, exchange_code: str = "NSE") -> bool:
        """
        Checks if the given timestamp falls on a holiday.
        
        Args:
            timestamp (datetime): The date/time to check.
            exchange_code (str): The exchange.
            
        Returns:
            bool: True if it's a holiday, False otherwise.
        """
        if self._exchange and self._exchange.exchange_code != exchange_code:
            return False # We only know about our bound exchange

        # Weekends are implicitly holidays for NSE
        if timestamp.weekday() >= 5: # 5=Sat, 6=Sun
            return True

        return timestamp.date() in self._holidays

    def is_expiry_day(self, timestamp: datetime, symbol: str) -> bool:
        """
        Checks if the given date is an expiry day for the symbol.
        
        Args:
            timestamp (datetime): The date to check.
            symbol (str): The canonical symbol.
            
        Returns:
            bool: True if it's an expiry day, False otherwise.
        """
        if symbol not in self._expiries:
            return False
            
        return timestamp.date() in self._expiries[symbol]
