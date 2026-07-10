from dataclasses import dataclass, field
from typing import Dict, List
from Backend.core.evidence_dtos.base import BasePlatformObject, ObjectRelationship, RelationshipType, Cardinality

@dataclass
class CrossMarketRelationship(BasePlatformObject):
    """Base class for all first-class DAG relationships in Cross-Market analysis."""
    target_asset: str = ""
    benchmark_asset: str = ""

@dataclass
class CorrelationRelationship(CrossMarketRelationship):
    correlation_coefficient: float = 0.0
    rolling_window: int = 0
    policy_used: str = "PEARSON"

@dataclass
class RelativeStrengthRelationship(CrossMarketRelationship):
    rs_ratio: float = 0.0
    is_outperforming: bool = True

@dataclass
class LeadLagRelationship(CrossMarketRelationship):
    lead_asset: str = ""
    lag_asset: str = ""
    lag_periods: int = 0

@dataclass
class CointegrationRelationship(CrossMarketRelationship):
    is_cointegrated: bool = False
    z_score: float = 0.0

@dataclass
class MarketBreadthObject(BasePlatformObject):
    """Dedicated object hierarchy for breadth."""
    universe_id: str = ""

@dataclass
class AdvanceDecline(MarketBreadthObject):
    advancing_issues: int = 0
    declining_issues: int = 0
    unchanged_issues: int = 0
    net_advances: int = 0
    
@dataclass
class NewHighNewLow(MarketBreadthObject):
    new_highs: int = 0
    new_lows: int = 0
    lookback_period: str = "52W"
