"""
Market Rotation Engine.

Performs sector ranking and dynamic priority filtering based on capital rotation.

Dependency Graph:
    Consumes: [MarketContextEngine, UniverseManager]
    Produces: [Sector Rankings]
    Registry: MarketIntelligenceRegistry (Future)
    Downstream: EvidenceEngine, OpportunityScanner
    Owner: MarketIntelligenceTeam
"""

from typing import Dict, List, Any
import pandas as pd

class MarketRotationEngine:
    """Analyzes and ranks sectors based on relative momentum and rotation."""

    def __init__(self, context_engine: Any = None, universe_manager: Any = None):
        """
        Initializes the Market Rotation Engine.
        
        Args:
            context_engine: Engine providing overarching market trend.
            universe_manager: Engine providing sector constituents.
        """
        self._context_engine = context_engine
        self._universe = universe_manager
        self._sector_scores: Dict[str, float] = {}

    def update_sector_scores(self, sector_data: Dict[str, pd.DataFrame]) -> None:
        """
        Evaluates the momentum of each sector index and updates their relative scores.
        
        Args:
            sector_data (Dict[str, pd.DataFrame]): A dictionary mapping sector names 
                                                   to their canonical dataframes.
        """
        for sector, df in sector_data.items():
            if df.empty or len(df) < 20:
                self._sector_scores[sector] = 0.0
                continue
                
            # Naive placeholder: Rate of change over the last 20 periods
            start_price = df['close'].iloc[-20]
            end_price = df['close'].iloc[-1]
            
            if start_price > 0:
                roc = (end_price - start_price) / start_price
                self._sector_scores[sector] = roc
            else:
                self._sector_scores[sector] = 0.0

    def get_ranked_sectors(self) -> List[str]:
        """
        Returns a list of sectors sorted by highest momentum to lowest.
        
        Returns:
            List[str]: Ranked sector names.
        """
        # Sort by score descending
        sorted_items = sorted(self._sector_scores.items(), key=lambda item: item[1], reverse=True)
        return [item[0] for item in sorted_items]

    def get_sector_score(self, sector: str) -> float:
        """Gets the raw momentum score for a specific sector."""
        return self._sector_scores.get(sector, 0.0)
