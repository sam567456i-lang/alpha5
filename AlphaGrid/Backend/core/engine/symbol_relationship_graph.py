from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class RelationshipEdge:
    primary_symbol_id: str
    secondary_symbol_id: str
    relationship_type: str # e.g. INDEX_CORRELATED, SECTOR_CORRELATED
    confidence: float
    weight: float

class SymbolRelationshipGraph:
    """
    Graph defining multi-asset relationships across the universe.
    Supports N-asset connections (e.g. BTC -> NASDAQ -> DXY -> GOLD).
    """
    def __init__(self):
        self._edges: List[RelationshipEdge] = []
        
    def add_edge(self, primary: str, secondary: str, rel_type: str, confidence: float = 1.0, weight: float = 1.0):
        self._edges.append(RelationshipEdge(primary, secondary, rel_type, confidence, weight))
        
    def get_related_symbols(self, symbol_id: str) -> List[RelationshipEdge]:
        return [e for e in self._edges if e.primary_symbol_id == symbol_id or e.secondary_symbol_id == symbol_id]
    
    def get_comparison_group(self, group_name: str) -> List[str]:
        # Stub for returning a group of N assets to compare
        if group_name == "US_INDICES":
            return ["ES", "NQ", "YM", "RTY"]
        return []
