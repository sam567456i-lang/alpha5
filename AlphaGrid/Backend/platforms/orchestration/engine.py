from typing import List, Dict, Any
from dataclasses import dataclass, field

@dataclass
class MarketProfile:
    market: str
    symbol: str
    timeframe: str
    style: str
    regime: str = "unknown"
    volatility: str = "unknown"
    trend: str = "unknown"
    volume: str = "unknown"

@dataclass
class CapabilityMetadata:
    id: str
    name: str
    supported_markets: List[str] = field(default_factory=lambda: ["all"])
    supported_styles: List[str] = field(default_factory=lambda: ["all"])
    supported_timeframes: List[str] = field(default_factory=lambda: ["all"])
    required_indicators: List[str] = field(default_factory=list)
    required_analysis: List[str] = field(default_factory=list)
    market_conditions: Dict[str, List[str]] = field(default_factory=dict)

class CapabilityOrchestrator:
    """
    Platform 7: Capability Selection & Orchestration
    Responsible for scanning the registries, filtering out unsupported capabilities 
    based on the MarketProfile, and compiling the dynamic DAG execution plan.
    """
    def __init__(self, registry_paths: Dict[str, str]):
        self.registry_paths = registry_paths
        self.active_capabilities: List[CapabilityMetadata] = []
        
    def load_registries(self):
        # Implementation to load all split YAML registries
        pass
        
    def filter_capabilities(self, profile: MarketProfile) -> List[CapabilityMetadata]:
        """Filters out analyses and strategies that don't match the current Market Profile."""
        eligible = []
        for cap in self.active_capabilities:
            # Check market
            if "all" not in cap.supported_markets and profile.market not in cap.supported_markets:
                continue
            # Check timeframe
            if "all" not in cap.supported_timeframes and profile.timeframe not in cap.supported_timeframes:
                continue
            # Check style
            if "all" not in cap.supported_styles and profile.style not in cap.supported_styles:
                continue
                
            # Check market conditions
            conditions_met = True
            for condition_key, allowed_values in cap.market_conditions.items():
                actual_value = getattr(profile, condition_key, None)
                if actual_value and "all" not in allowed_values and actual_value not in allowed_values:
                    conditions_met = False
                    break
                    
            if conditions_met:
                eligible.append(cap)
                
        return eligible
        
    def build_execution_graph(self, profile: MarketProfile) -> Dict[str, Any]:
        """Constructs the final DAG for the downstream engines (AnalysisEngine, ConceptEngine)."""
        eligible = self.filter_capabilities(profile)
        # DAG compilation logic goes here
        return {"plan": eligible}
