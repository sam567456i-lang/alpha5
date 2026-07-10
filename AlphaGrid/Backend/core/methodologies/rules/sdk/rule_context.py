from dataclasses import dataclass
from typing import List, Dict, Any
from Backend.core.data_foundation.contracts.schemas import OHLCSchema

@dataclass
class RuleContext:
    """The canonical input state passed to every Evidence Rule."""
    historical_bars: List[OHLCSchema]
    current_bar: OHLCSchema
    market_regime: str
    active_dataset_id: str
    parameters: Dict[str, Any]

@dataclass
class RuleResult:
    """The canonical output state emitted by every Evidence Rule."""
    did_trigger: bool
    evidence: Any = None # Instance of RuleEvidence
