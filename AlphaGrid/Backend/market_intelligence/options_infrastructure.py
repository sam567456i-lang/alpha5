"""
Options Market Infrastructure.

Provides the foundational placeholder interfaces for the future 
Options Research Platform. Explicitly deferred from analytics calculation 
in Phase 10B.

Dependency Graph:
    Consumes: []
    Produces: [AbstractOptionChainProvider, OptionInstrumentResolver, ExpiryResolver]
    Registry: MarketIntelligenceRegistry (Future)
    Downstream: OptionsResearchPlatform (Future)
    Owner: MarketIntelligenceTeam
"""

import abc
from datetime import datetime, date
from typing import List, Optional
import pandas as pd


class AbstractOptionChainProvider(abc.ABC):
    """Base interface for fetching Option Chains."""

    @abc.abstractmethod
    def get_chain(self, underlying_symbol: str, expiry: date) -> pd.DataFrame:
        """
        Retrieves the option chain (calls and puts) for a specific expiry.
        
        Args:
            underlying_symbol (str): The canonical underlying symbol.
            expiry (date): The exact expiry date.
            
        Returns:
            pd.DataFrame: DataFrame containing strike, type (CE/PE), price, volume, OI.
        """
        pass


class OptionInstrumentResolver(abc.ABC):
    """Resolves specific option instrument symbols from underlying context."""

    @abc.abstractmethod
    def resolve_symbol(self, underlying_symbol: str, expiry: date, strike: float, option_type: str) -> str:
        """
        Constructs the canonical broker/exchange specific symbol for an option.
        (e.g., 'NIFTY' + expiry + strike + 'CE' -> 'NIFTY26JUL15000CE')
        
        Args:
            underlying_symbol (str): The canonical underlying.
            expiry (date): The expiry date.
            strike (float): The strike price.
            option_type (str): 'CE' or 'PE'.
            
        Returns:
            str: The canonical option symbol.
        """
        pass


class ExpiryResolver(abc.ABC):
    """Resolves upcoming expiry dates for option contracts."""

    @abc.abstractmethod
    def get_next_expiry(self, underlying_symbol: str, current_date: date, cycle: str = "WEEKLY") -> date:
        """
        Determines the next expiry date for a given underlying.
        
        Args:
            underlying_symbol (str): The canonical underlying.
            current_date (date): The current date context.
            cycle (str): "WEEKLY" or "MONTHLY".
            
        Returns:
            date: The resolved expiry date.
        """
        pass

    @abc.abstractmethod
    def get_all_active_expiries(self, underlying_symbol: str, current_date: date) -> List[date]:
        """Returns all currently active expiry dates for the underlying."""
        pass
