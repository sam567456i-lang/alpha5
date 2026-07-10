from dataclasses import dataclass
from typing import Dict, Optional, List
from enum import Enum

class AssetClass(Enum):
    EQUITY = "EQUITY"
    CRYPTO = "CRYPTO"
    FOREX = "FOREX"
    FUTURES = "FUTURES"
    OPTIONS = "OPTIONS"

@dataclass(frozen=True)
class SymbolMetadata:
    """Canonical mapping for an individual asset across all vendors."""
    canonical_id: str
    exchange: str
    venue: str
    currency: str
    tick_size: float
    lot_size: float
    multiplier: float
    contract_type: str
    expiration: Optional[str]
    asset_class: AssetClass
    underlying: Optional[str]
    sector: Optional[str]
    industry: Optional[str]

class SymbolRegistry:
    """Stores the canonical definition of all tradable assets."""
    def __init__(self):
        self._symbols: Dict[str, SymbolMetadata] = {}
        
    def register_symbol(self, metadata: SymbolMetadata):
        self._symbols[metadata.canonical_id] = metadata
        
    def get_symbol(self, canonical_id: str) -> SymbolMetadata:
        if canonical_id not in self._symbols:
            raise KeyError(f"Symbol {canonical_id} not found in Registry.")
        return self._symbols[canonical_id]
