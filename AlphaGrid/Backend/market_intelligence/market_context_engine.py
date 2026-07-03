"""
Market Context Engine.

Evaluates the overarching market context, such as VIX, Market Breadth,
and macroscopic Trend identification.

Dependency Graph:
    Consumes: [Canonical OHLCV DataFrame, UniverseManager]
    Produces: [MarketContext]
    Registry: MarketIntelligenceRegistry (Future)
    Downstream: MarketRotationEngine, FeatureEngine, EvidenceEngine
    Owner: MarketIntelligenceTeam
"""

import pandas as pd
from typing import Dict, Any, Optional
from enum import Enum

class TrendState(Enum):
    BULL_STRONG = "BULL_STRONG"
    BULL_WEAK = "BULL_WEAK"
    BEAR_STRONG = "BEAR_STRONG"
    BEAR_WEAK = "BEAR_WEAK"
    SIDEWAYS = "SIDEWAYS"
    VOLATILE = "VOLATILE"

class MarketContextEngine:
    """Evaluates and provides the macroscopic market context."""

    def __init__(self, universe_manager: Any = None):
        """
        Initializes the Market Context Engine.
        
        Args:
            universe_manager: The manager to query for the market universe.
        """
        self._universe = universe_manager
        self._vix_cache: Dict[str, float] = {}

    def update_vix(self, symbol: str, current_value: float) -> None:
        """Updates the internal cache with the latest VIX value."""
        self._vix_cache[symbol] = current_value

    def get_market_trend(self, index_df: pd.DataFrame) -> TrendState:
        """
        Determines the broad market trend using a simple heuristic (e.g. SMA crossovers).
        This is a placeholder for a more sophisticated regime model.
        
        Args:
            index_df (pd.DataFrame): The canonical dataframe for the benchmark index (e.g. NIFTY).
            
        Returns:
            TrendState: The evaluated trend.
        """
        if index_df.empty or len(index_df) < 50:
            return TrendState.SIDEWAYS
            
        # Very naive implementation for scaffolding
        close = index_df['close']
        sma_20 = close.rolling(window=20).mean().iloc[-1]
        sma_50 = close.rolling(window=50).mean().iloc[-1]
        last_close = close.iloc[-1]
        
        if last_close > sma_20 > sma_50:
            return TrendState.BULL_STRONG
        elif last_close < sma_20 < sma_50:
            return TrendState.BEAR_STRONG
            
        return TrendState.SIDEWAYS

    def get_breadth(self, advances: int, declines: int) -> float:
        """
        Calculates the Advance/Decline ratio or Breadth.
        
        Args:
            advances (int): Number of advancing issues.
            declines (int): Number of declining issues.
            
        Returns:
            float: A ratio representing market breadth.
        """
        if declines == 0:
            return float('inf') if advances > 0 else 1.0
        return advances / declines
