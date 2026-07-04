from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import pandas as pd

@dataclass
class AnalysisContext:
    """Universal context injected into every analysis."""
    market_data: pd.DataFrame
    timeframe: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    dependencies: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AnalysisResult:
    """Universal output from every analysis."""
    score: float
    raw_data: pd.DataFrame
    signals: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AnalysisMetadata:
    """Representation of the Governance capability registry entry."""
    capability_id: str
    platform: str
    family: str
    subfamily: str
    dependencies: List[str]
