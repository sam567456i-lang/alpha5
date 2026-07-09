from dataclasses import dataclass, field
from typing import Dict, List, Optional
from Backend.core.analytical_rules.capabilities.evidence_graph import EvidenceGraph

@dataclass
class MultiTimeframeEvidenceGraph:
    """
    Wraps individual EvidenceGraphs keyed by timeframe.
    Ensures that methodologies consume synchronized multi-timeframe context.
    """
    # Keyed by standard intervals: '1M', '5M', '15M', '1H', '4H', '1D', '1W', '1MN'
    graphs: Dict[str, EvidenceGraph] = field(default_factory=dict)
    
    def timeframe(self, tf: str) -> Optional[EvidenceGraph]:
        """Retrieve the objective evidence graph for a specific timeframe."""
        return self.graphs.get(tf.upper())
        
    def available_timeframes(self) -> List[str]:
        """List all timeframes loaded in this snapshot."""
        return list(self.graphs.keys())
        
    def add_timeframe(self, tf: str, graph: EvidenceGraph) -> None:
        """Register an EvidenceGraph for a timeframe."""
        self.graphs[tf.upper()] = graph
