from typing import List
from Backend.core.engine.symbol_relationship_graph import SymbolRelationshipGraph
from Backend.core.analytical_rules.dto.cross_market_evidence_dto import CorrelationEvidenceDTO, LeadLagEvidenceDTO

class CrossMarketAnalyticsEngine:
    """
    Computes objective relationship evidence (correlation, cointegration, lead/lag, etc.)
    between multiple symbols using the SymbolRelationshipGraph.
    """
    def __init__(self, graph: SymbolRelationshipGraph):
        self.graph = graph
        
    def compute_relationships(self, primary_symbol: str) -> List:
        edges = self.graph.get_related_symbols(primary_symbol)
        evidence_list = []
        
        for edge in edges:
            secondary = edge.secondary_symbol_id if edge.primary_symbol_id == primary_symbol else edge.primary_symbol_id
            
            # Emit Correlation Evidence
            corr_ev = CorrelationEvidenceDTO(
                identity=None, metadata=None, provenance=None, classification=None, interpretation_level=None, validity_status=None, evidence_data={},
                primary_symbol_id=primary_symbol,
                secondary_symbol_id=secondary,
                correlation_coefficient=0.85 * edge.weight, # dummy calculation
                rolling_window=20,
                metric_type="PEARSON"
            )
            evidence_list.append(corr_ev)
            
            # Emit Lead/Lag Evidence
            ll_ev = LeadLagEvidenceDTO(
                identity=None, metadata=None, provenance=None, classification=None, interpretation_level=None, validity_status=None, evidence_data={},
                primary_symbol_id=primary_symbol,
                secondary_symbol_id=secondary,
                leader_symbol_id=primary_symbol,
                lag_periods=1,
                confidence=edge.confidence
            )
            evidence_list.append(ll_ev)
            
        return evidence_list
