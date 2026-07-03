"""
Market Universe Manager.

Authoritative source of truth for all downstream scanners.
Manages the tiered hierarchy of tradable symbols (Tier A, Tier B, etc.).

Dependency Graph:
    Consumes: [SymbolMetadataRegistry]
    Produces: [Universe Lists]
    Registry: MarketIntelligenceRegistry (Future)
    Downstream: FeatureEngine, OpportunityScanner
    Owner: MarketIntelligenceTeam
"""

from typing import List, Dict, Optional, Any
from enum import Enum

class UniverseTier(Enum):
    TIER_A = "TIER_A" # Always Scanned: NIFTY, BANKNIFTY, FINNIFTY, MIDCPNIFTY
    TIER_B = "TIER_B" # Top 100 NSE F&O Stocks
    TIER_C = "TIER_C" # Sector Indices
    TIER_D = "TIER_D" # Validation Only: SPY, QQQ, EURUSD
    TIER_E = "TIER_E" # Future: Crypto

class UniverseManager:
    """Manages tiered symbol universes."""

    def __init__(self, metadata_registry: Optional[Any] = None):
        """
        Initializes the Universe Manager.
        
        Args:
            metadata_registry (SymbolMetadataRegistry): The registry for symbol metadata.
        """
        self._registry = metadata_registry
        self._tiers: Dict[UniverseTier, List[str]] = {
            UniverseTier.TIER_A: [],
            UniverseTier.TIER_B: [],
            UniverseTier.TIER_C: [],
            UniverseTier.TIER_D: [],
            UniverseTier.TIER_E: []
        }

    def assign_to_tier(self, symbol: str, tier: UniverseTier) -> None:
        """Assigns a symbol to a specific tier."""
        if symbol not in self._tiers[tier]:
            self._tiers[tier].append(symbol)

    def remove_from_tier(self, symbol: str, tier: UniverseTier) -> None:
        """Removes a symbol from a specific tier."""
        if symbol in self._tiers[tier]:
            self._tiers[tier].remove(symbol)

    def get_tier(self, tier: UniverseTier) -> List[str]:
        """Gets all symbols in a specific tier."""
        return list(self._tiers[tier])

    def get_all_scannable(self) -> List[str]:
        """Gets all symbols from Tier A, B, and C that should be actively scanned."""
        symbols = set()
        symbols.update(self._tiers[UniverseTier.TIER_A])
        symbols.update(self._tiers[UniverseTier.TIER_B])
        symbols.update(self._tiers[UniverseTier.TIER_C])
        return list(symbols)

    def is_validation_only(self, symbol: str) -> bool:
        """Checks if a symbol is restricted to validation testing only (Tier D)."""
        return symbol in self._tiers[UniverseTier.TIER_D]
