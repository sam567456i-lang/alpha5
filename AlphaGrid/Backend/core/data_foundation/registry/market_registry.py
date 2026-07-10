from dataclasses import dataclass
from typing import Dict, List, Optional
from Backend.core.data_foundation.contracts.schemas import MarketType

class RegistryException(Exception):
    pass

@dataclass(frozen=True)
class TimezoneDefinition:
    id: str
    iana_name: str
    utc_offset: str

class TimezoneRegistry:
    def __init__(self):
        self._items: Dict[str, TimezoneDefinition] = {}
        
    def register(self, definition: TimezoneDefinition):
        if definition.id in self._items:
            raise RegistryException(f"Timezone {definition.id} already registered.")
        self._items[definition.id] = definition
        
    def get(self, id: str) -> TimezoneDefinition:
        if id not in self._items:
            raise RegistryException(f"Timezone {id} not found.")
        return self._items[id]

@dataclass(frozen=True)
class CurrencyDefinition:
    id: str
    name: str
    symbol: str

class CurrencyRegistry:
    def __init__(self):
        self._items: Dict[str, CurrencyDefinition] = {}
        
    def register(self, definition: CurrencyDefinition):
        if definition.id in self._items:
            raise RegistryException(f"Currency {definition.id} already registered.")
        self._items[definition.id] = definition
        
    def get(self, id: str) -> CurrencyDefinition:
        if id not in self._items:
            raise RegistryException(f"Currency {id} not found.")
        return self._items[id]

@dataclass(frozen=True)
class CalendarDefinition:
    id: str
    description: str

class CalendarRegistry:
    def __init__(self):
        self._items: Dict[str, CalendarDefinition] = {}
        
    def register(self, definition: CalendarDefinition):
        if definition.id in self._items:
            raise RegistryException(f"Calendar {definition.id} already registered.")
        self._items[definition.id] = definition
        
    def get(self, id: str) -> CalendarDefinition:
        if id not in self._items:
            raise RegistryException(f"Calendar {id} not found.")
        return self._items[id]

@dataclass(frozen=True)
class TickSizeDefinition:
    id: str
    value: float

class TickSizeRegistry:
    def __init__(self):
        self._items: Dict[str, TickSizeDefinition] = {}
        
    def register(self, definition: TickSizeDefinition):
        if definition.id in self._items:
            raise RegistryException(f"TickSize {definition.id} already registered.")
        self._items[definition.id] = definition
        
    def get(self, id: str) -> TickSizeDefinition:
        if id not in self._items:
            raise RegistryException(f"TickSize {id} not found.")
        return self._items[id]

@dataclass(frozen=True)
class ExchangeDefinition:
    id: str
    name: str
    country: str
    market_types: List[MarketType]

class ExchangeRegistry:
    def __init__(self):
        self._items: Dict[str, ExchangeDefinition] = {}
        
    def register(self, definition: ExchangeDefinition):
        if definition.id in self._items:
            raise RegistryException(f"Exchange {definition.id} already registered.")
        self._items[definition.id] = definition
        
    def get(self, id: str) -> ExchangeDefinition:
        if id not in self._items:
            raise RegistryException(f"Exchange {id} not found.")
        return self._items[id]

@dataclass(frozen=True)
class MarketMetadata:
    market_id: str
    exchange_id: str
    market_type: MarketType
    trading_hours: str
    session_rules: str
    holiday_calendar_id: str
    timezone_id: str
    currency_id: str
    tick_size_id: str
    lot_size: float
    asset_type: str

class MarketRegistry:
    def __init__(self):
        self._items: Dict[str, MarketMetadata] = {}
        
    def register(self, definition: MarketMetadata):
        if definition.market_id in self._items:
            raise RegistryException(f"Market {definition.market_id} already registered.")
        self._items[definition.market_id] = definition
        
    def get(self, id: str) -> MarketMetadata:
        if id not in self._items:
            raise RegistryException(f"Market {id} not found.")
        return self._items[id]
