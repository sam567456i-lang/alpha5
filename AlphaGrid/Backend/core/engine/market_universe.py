from typing import Dict, Optional, List
from Backend.core.analytical_rules.capabilities.evidence_graph import EvidenceGraph
from Backend.core.engine.symbol_identity import SymbolIdentity

class MarketUniverse:
    """
    Central registry owning all multi-timeframe graphs across all tracked symbols.
    """
    def __init__(self):
        self._symbol_identities: Dict[str, SymbolIdentity] = {}
        self._symbol_graphs: Dict[str, EvidenceGraph] = {}
        
    def register_symbol(self, identity: SymbolIdentity, graph: EvidenceGraph):
        self._symbol_identities[identity.id] = identity
        self._symbol_graphs[identity.id] = graph
        
    def get_identity(self, symbol_id: str) -> Optional[SymbolIdentity]:
        return self._symbol_identities.get(symbol_id)
        
    def get_graph(self, symbol_id: str) -> Optional[EvidenceGraph]:
        return self._symbol_graphs.get(symbol_id)
        
    def get_all_symbols(self) -> List[str]:
        return list(self._symbol_identities.keys())


class MultiMarketEvidenceGraph:
    """
    The query layer on top of MarketUniverse, providing cross-market data access.
    """
    def __init__(self, universe: MarketUniverse):
        self.universe = universe
        
    def query_evidence(self, symbol_id: str, timeframe: str = None) -> List:
        """
        Query evidence from a specific symbol's graph.
        """
        graph = self.universe.get_graph(symbol_id)
        if not graph:
            return []
            
        if timeframe:
            return graph.get_evidence_by_timeframe(timeframe)
        return graph.get_all_evidence()
