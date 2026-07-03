"""
Symbol Metadata Registry.

Stores rich metadata for every tradable instrument. This is the canonical source
for instrument properties (lot size, tick size, sector, margin class, etc.).

Dependency Graph:
    Consumes: []
    Produces: [SymbolMetadata]
    Registry: MarketIntelligenceRegistry (Future)
    Downstream: UniverseManager, NormalizationEngine
    Owner: MarketIntelligenceTeam
"""

from dataclasses import dataclass
from typing import Dict, Optional, List
from enum import Enum
from Backend.foundation.base_registry import BaseRegistry

class InstrumentType(Enum):
    EQUITY = "EQUITY"
    INDEX = "INDEX"
    FUTURE = "FUTURE"
    OPTION = "OPTION"
    FOREX = "FOREX"
    CRYPTO = "CRYPTO"

@dataclass
class SymbolMetadata:
    """Canonical metadata for a single instrument."""
    canonical_symbol: str
    instrument_type: InstrumentType
    exchange: str
    sector: Optional[str] = None
    industry: Optional[str] = None
    tick_size: float = 0.05
    lot_size: int = 1
    margin_class: Optional[str] = None
    expiry_cycle: Optional[str] = None
    currency: str = "INR"
    trading_hours_id: str = "DEFAULT"

class SymbolMetadataRegistry(BaseRegistry[SymbolMetadata]):
    """Registry containing metadata for all known symbols."""

    def __init__(self):
        super().__init__("SymbolMetadataRegistry", version="1.0.0")

    def register(self, metadata: SymbolMetadata) -> None:
        """Registers metadata for a symbol."""
        super().register(metadata.canonical_symbol, metadata)

    def get_by_sector(self, sector: str) -> List[SymbolMetadata]:
        """Returns metadata for all symbols in a specific sector."""
        return [m for m in self.get_all() if m.sector == sector]
