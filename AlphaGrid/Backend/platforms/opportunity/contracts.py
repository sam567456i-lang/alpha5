from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import uuid

@dataclass
class Opportunity:
    # Core Identity
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    market: str = ""
    symbol: str = ""
    timeframe: str = ""
    strategy: str = ""
    
    # Trade Mechanics
    entry: float = 0.0
    stop: float = 0.0
    target: float = 0.0
    rr: float = 0.0
    
    # Validation & Probability
    confidence: float = 0.0
    probability: float = 0.0
    risk: float = 0.0
    
    # Provenance (Audit Trail)
    analysis_used: List[str] = field(default_factory=list)
    concepts_used: List[str] = field(default_factory=list)
    signals_used: List[str] = field(default_factory=list)
    
    # Rich Context
    evidence: Dict[str, Any] = field(default_factory=dict)
    ai_summary: Optional[str] = None
    data_quality_score: float = 1.0  # Added per user spec
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "market": self.market,
            "symbol": self.symbol,
            "timeframe": self.timeframe,
            "strategy": self.strategy,
            "entry": self.entry,
            "stop": self.stop,
            "target": self.target,
            "rr": self.rr,
            "confidence": self.confidence,
            "probability": self.probability,
            "risk": self.risk,
            "analysis_used": self.analysis_used,
            "concepts_used": self.concepts_used,
            "signals_used": self.signals_used,
            "evidence": self.evidence,
            "ai_summary": self.ai_summary,
            "data_quality_score": self.data_quality_score
        }
