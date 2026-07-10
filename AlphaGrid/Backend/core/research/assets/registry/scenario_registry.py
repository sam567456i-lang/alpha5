from dataclasses import dataclass
from typing import List, Optional
from enum import Enum

class MarketRegime(Enum):
    TRENDING = "TRENDING"
    RANGING = "RANGING"
    HIGH_VOLATILITY = "HIGH_VOLATILITY"
    LOW_VOLATILITY = "LOW_VOLATILITY"
    BULL = "BULL"
    BEAR = "BEAR"
    SIDEWAYS = "SIDEWAYS"
    NEWS_EVENT = "NEWS_EVENT"
    GAP = "GAP"
    FLASH_CRASH = "FLASH_CRASH"
    CRYPTO_WEEKEND = "CRYPTO_WEEKEND"
    FUTURES_ROLLOVER = "FUTURES_ROLLOVER"

@dataclass(frozen=True)
class ScenarioMetadata:
    """Catalog entry for a specific research scenario."""
    scenario_id: str
    name: str
    description: str
    regime: MarketRegime
    asset_class: str
    timeframe: str
    dataset_version: str
    tags: List[str]

class ScenarioRegistry:
    """Searchable catalog mapping expected setups to specific market regimes."""
    
    def __init__(self):
        self._scenarios = {}
        
    def register(self, metadata: ScenarioMetadata):
        self._scenarios[metadata.scenario_id] = metadata
        
    def search_by_regime(self, regime: MarketRegime) -> List[ScenarioMetadata]:
        return [s for s in self._scenarios.values() if s.regime == regime]
