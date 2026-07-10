from dataclasses import dataclass
from typing import Dict, Optional
from Backend.core.data_foundation.registry.market_registry import RegistryException

@dataclass(frozen=True)
class SymbolDefinition:
    """Canonical mapping for an individual asset referencing the MarketRegistry."""
    internal_symbol_id: str
    market_id: str  # References MarketMetadata in MarketRegistry
    vendor_symbol: str
    base_asset: str
    quote_asset: str
    expiration: Optional[str] = None
    strike_price: Optional[float] = None
    option_type: Optional[str] = None # "CALL", "PUT"

class SymbolRegistry:
    """Stores the programmatic definition of all tradable assets."""
    def __init__(self):
        self._items: Dict[str, SymbolDefinition] = {}
        
    def register(self, definition: SymbolDefinition):
        if definition.internal_symbol_id in self._items:
            raise RegistryException(f"Symbol {definition.internal_symbol_id} already registered.")
        self._items[definition.internal_symbol_id] = definition
        
    def get(self, id: str) -> SymbolDefinition:
        if id not in self._items:
            raise RegistryException(f"Symbol {id} not found.")
        return self._items[id]
