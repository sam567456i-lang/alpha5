"""
Market Data Provider Abstractions.

This module defines the abstract interfaces for all market data providers.
All Market Intelligence modules must depend ONLY on these interfaces, never
on concrete vendor implementations.

Dependency Graph:
    Consumes: []
    Produces: [AbstractMarketDataProvider, HistoricalDataProvider, LiveDataProvider, OptionDataProvider, EconomicCalendarProvider, NewsProvider]
    Registry: DataProviderRegistry (Future)
    Downstream: NormalizationEngine, UniverseManager
    Owner: MarketIntelligenceTeam
"""

import abc
from typing import List, Dict, Any, Optional
from datetime import datetime
import pandas as pd


class AbstractMarketDataProvider(abc.ABC):
    """Base interface for all market data providers."""

    @property
    @abc.abstractmethod
    def provider_id(self) -> str:
        """Returns a unique identifier for this provider (e.g., 'YAHOO', 'IBKR')."""
        pass

    @property
    @abc.abstractmethod
    def dataset_version(self) -> str:
        """Returns the version of the dataset being provided."""
        pass


class HistoricalDataProvider(AbstractMarketDataProvider):
    """Interface for retrieving historical OHLCV data."""

    @abc.abstractmethod
    def get_historical_bars(
        self,
        symbol: str,
        start_time: datetime,
        end_time: datetime,
        timeframe: str
    ) -> pd.DataFrame:
        """
        Retrieves historical bars for a given symbol and timeframe.

        Args:
            symbol (str): The canonical symbol (e.g., 'NIFTY').
            start_time (datetime): The start timestamp.
            end_time (datetime): The end timestamp.
            timeframe (str): The timeframe resolution (e.g., '1m', '1D').

        Returns:
            pd.DataFrame: A DataFrame containing the raw OHLCV data.
        """
        pass


class LiveDataProvider(AbstractMarketDataProvider):
    """Interface for subscribing to real-time market data streams."""

    @abc.abstractmethod
    def subscribe(self, symbols: List[str], callback: callable) -> None:
        """
        Subscribes to live tick or bar updates for the given symbols.

        Args:
            symbols (List[str]): List of canonical symbols.
            callback (callable): Function to call when data arrives.
        """
        pass

    @abc.abstractmethod
    def unsubscribe(self, symbols: List[str]) -> None:
        """Unsubscribes from live data for the given symbols."""
        pass


class OptionDataProvider(AbstractMarketDataProvider):
    """Interface for retrieving options market data."""

    @abc.abstractmethod
    def get_option_chain(
        self,
        underlying_symbol: str,
        expiry_date: datetime
    ) -> pd.DataFrame:
        """
        Retrieves the option chain for a specific underlying and expiry.

        Args:
            underlying_symbol (str): The canonical underlying symbol.
            expiry_date (datetime): The expiry date.

        Returns:
            pd.DataFrame: A DataFrame containing the option chain data (strikes, prices, etc.).
        """
        pass


class EconomicCalendarProvider(AbstractMarketDataProvider):
    """Interface for retrieving economic events and calendars."""

    @abc.abstractmethod
    def get_economic_events(
        self,
        start_time: datetime,
        end_time: datetime,
        countries: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Retrieves economic events within a time range.

        Args:
            start_time (datetime): The start timestamp.
            end_time (datetime): The end timestamp.
            countries (Optional[List[str]]): Filter by country codes (e.g., ['IN', 'US']).

        Returns:
            pd.DataFrame: A DataFrame containing event details, impact, and estimates.
        """
        pass


class NewsProvider(AbstractMarketDataProvider):
    """Interface for retrieving market news and sentiment data."""

    @abc.abstractmethod
    def get_news(
        self,
        symbols: Optional[List[str]],
        start_time: datetime,
        end_time: datetime
    ) -> pd.DataFrame:
        """
        Retrieves news articles and headlines.

        Args:
            symbols (Optional[List[str]]): Filter by symbols.
            start_time (datetime): The start timestamp.
            end_time (datetime): The end timestamp.

        Returns:
            pd.DataFrame: A DataFrame containing news headlines, timestamps, and sources.
        """
        pass
