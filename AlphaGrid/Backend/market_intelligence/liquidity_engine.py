"""
Liquidity Engine.

Analyzes bid/ask spread, volume profiles, and estimates slippage.
Provides a filter to reject symbols with inadequate liquidity.

Dependency Graph:
    Consumes: [Canonical OHLCV DataFrame]
    Produces: [Liquidity Metrics]
    Registry: MarketIntelligenceRegistry (Future)
    Downstream: OpportunityScanner, FeatureEngine
    Owner: MarketIntelligenceTeam
"""

import pandas as pd
from typing import Dict, Any

class LiquidityEngine:
    """Evaluates instrument liquidity and estimates slippage."""

    def __init__(self, minimum_volume: float = 100000.0, max_acceptable_spread_pct: float = 0.005):
        """
        Initializes the Liquidity Engine.
        
        Args:
            minimum_volume (float): Minimum acceptable daily volume (in currency).
            max_acceptable_spread_pct (float): Maximum spread as a percentage of price.
        """
        self._min_volume = minimum_volume
        self._max_spread_pct = max_acceptable_spread_pct

    def is_liquid(self, df: pd.DataFrame) -> bool:
        """
        Checks if the instrument meets the minimum liquidity threshold based on recent history.
        
        Args:
            df (pd.DataFrame): The canonical dataframe for the instrument.
            
        Returns:
            bool: True if liquid enough to trade, False otherwise.
        """
        if df.empty or len(df) < 5:
            return False
            
        # Using a simple 5-period average volume check
        recent_volume = df['volume'].tail(5).mean()
        
        # If price is available, we can approximate monetary volume:
        recent_price = df['close'].tail(5).mean()
        monetary_volume = recent_volume * recent_price
        
        return monetary_volume >= self._min_volume

    def estimate_slippage(self, df: pd.DataFrame, order_size: float) -> float:
        """
        Estimates expected slippage as a percentage based on historical liquidity profile.
        
        Args:
            df (pd.DataFrame): The canonical dataframe.
            order_size (float): The size of the intended order (in currency).
            
        Returns:
            float: Expected slippage percentage.
        """
        if df.empty:
            return self._max_spread_pct
            
        # Very naive placeholder: Higher order size relative to average volume -> higher slippage
        avg_vol = df['volume'].mean() * df['close'].mean()
        if avg_vol == 0:
            return self._max_spread_pct
            
        ratio = order_size / avg_vol
        
        # Base slippage of 0.05% + impact of order size
        slippage = 0.0005 + (ratio * 0.01)
        
        return min(slippage, self._max_spread_pct)
