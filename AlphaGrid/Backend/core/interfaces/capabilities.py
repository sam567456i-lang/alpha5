from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Set

class CapabilityLevel(Enum):
    REQUIRED = "REQUIRED"
    OPTIONAL = "OPTIONAL"
    SUPPORTED = "SUPPORTED"
    UNSUPPORTED = "UNSUPPORTED"
    DEGRADED = "DEGRADED"

class FeedCapability(Enum):
    OHLC = "OHLC"
    VOLUME = "VOLUME"
    TICK = "TICK"
    TRADE = "TRADE"
    QUOTE = "QUOTE"
    LEVEL1 = "LEVEL1"
    LEVEL2 = "LEVEL2"
    MBO = "MBO"
    OPTIONS = "OPTIONS"
    ECONOMIC_CALENDAR = "ECONOMIC_CALENDAR"
    CROSS_MARKET = "CROSS_MARKET"
    CORPORATE_ACTIONS = "CORPORATE_ACTIONS"

@dataclass(frozen=True)
class FeedManifest:
    """The capabilities provided by the incoming market data feed."""
    provider_name: str
    capabilities: Set[FeedCapability]

@dataclass
class EngineCapabilityNegotiator:
    """
    Dynamically maps available feed capabilities to the engine's modules.
    Enables graceful degradation (disabling features) instead of engine crashes.
    """
    engine_name: str
    feed: FeedManifest
    active_modules: Set[str] = field(default_factory=set)
    unsupported_modules: Set[str] = field(default_factory=set)
    
    def negotiate_module(self, module_name: str, required: Set[FeedCapability], optional: Set[FeedCapability] = None) -> CapabilityLevel:
        """
        Determines if a module can operate given the current feed.
        """
        if optional is None:
            optional = set()
            
        missing_required = required - self.feed.capabilities
        if missing_required:
            self.unsupported_modules.add(module_name)
            return CapabilityLevel.UNSUPPORTED
            
        self.active_modules.add(module_name)
        
        missing_optional = optional - self.feed.capabilities
        if missing_optional:
            return CapabilityLevel.DEGRADED
            
        return CapabilityLevel.SUPPORTED
