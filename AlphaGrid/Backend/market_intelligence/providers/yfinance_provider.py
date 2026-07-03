"""Yahoo Finance Concrete Market Data Provider."""

from __future__ import annotations

import logging
from datetime import datetime
from typing import ClassVar

import pandas as pd
import yfinance as yf

from Backend.foundation.exceptions import DataError
from Backend.market_intelligence.providers.abstract_market_data_provider import HistoricalDataProvider

logger = logging.getLogger("alphagrid.providers.yfinance")


class YFinanceProvider(HistoricalDataProvider):
    """Yahoo Finance implementation of the HistoricalDataProvider interface.
    
    This provider uses the 'yfinance' library to download historical OHLCV 
    data directly from Yahoo Finance without any local caching.
    """
    
    _TIMEFRAME_MAP: ClassVar[dict[str, str]] = {
        "1m": "1m",
        "5m": "5m",
        "15m": "15m",
        "30m": "30m",
        "1h": "1h",
        "1D": "1d",
        "1W": "1wk",
        "1M": "1mo",
    }

    @property
    def provider_id(self) -> str:
        return "YFINANCE"

    @property
    def dataset_version(self) -> str:
        return "1.0.0"

    def get_historical_bars(
        self,
        symbol: str,
        start_time: datetime,
        end_time: datetime,
        timeframe: str
    ) -> pd.DataFrame:
        if timeframe not in self._TIMEFRAME_MAP:
            raise DataError(f"Timeframe '{timeframe}' is not supported by YFinanceProvider.")
            
        yf_interval = self._TIMEFRAME_MAP[timeframe]
        
        logger.info(f"YFinanceProvider fetching {symbol} from {start_time} to {end_time} at {timeframe}")
        
        try:
            # yfinance expects symbol and dates
            ticker = yf.Ticker(symbol)
            df = ticker.history(
                start=start_time,
                end=end_time,
                interval=yf_interval,
                auto_adjust=False  # We want raw OHLCV for the downstream NormalizationEngine
            )
            
            if df.empty:
                logger.warning(f"YFinance returned empty DataFrame for {symbol}.")
                return pd.DataFrame()
            
            # yfinance returns columns like 'Open', 'High', 'Low', 'Close', 'Volume'
            # We standardize to lowercase for the canonical pipeline
            df = df.rename(columns={
                "Open": "open",
                "High": "high",
                "Low": "low",
                "Close": "close",
                "Volume": "volume"
            })
            
            return df
            
        except Exception as e:
            logger.error(f"YFinanceProvider failed to fetch data for {symbol}: {e}")
            raise DataError(f"Provider network error: {e}") from e

from Backend.market_intelligence.providers.provider_factory import ProviderFactory
ProviderFactory.register("yfinance", YFinanceProvider)
