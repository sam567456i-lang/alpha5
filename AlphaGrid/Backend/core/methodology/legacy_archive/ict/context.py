import uuid
from typing import List, Optional
from Backend.core.methodology.multi_timeframe_graph import MultiTimeframeEvidenceGraph
from Backend.core.methodology.narrative_node import BiasNode, POINode
from Backend.core.methodology.narrative_types import NarrativeNodeType, MethodologyType
from Backend.core.methodology.narrative_graph import NarrativeGraph

class ICTContextModule:
    """
    Evaluates Higher Timeframe Context (Bias and POIs) for the ICT Methodology.
    Does not compute geometry, only queries the EvidenceGraph.
    """
    
    def __init__(self, htf_intervals: List[str] = ["1D", "4H"]):
        self.htf_intervals = htf_intervals
        
    def evaluate_bias(self, mtf_graph: MultiTimeframeEvidenceGraph) -> BiasNode:
        """
        Determines directional bias by checking structural and liquidity evidence on HTF.
        """
        # Collect supporting evidence IDs
        supporting_evidence = []
        
        # Stub logic: Query the HTF graphs for structural trends and unmitigated liquidity.
        # If HTF structure is bullish and HTF SSL is swept, Bias -> Bullish.
        has_structure = False
        has_liquidity = False
        has_regions = False
        
        for tf in self.htf_intervals:
            graph = mtf_graph.timeframe(tf)
            if graph:
                # We would query graph.filter(...) here to find real evidence.
                # For now, we simulate finding evidence.
                has_structure = True
                has_liquidity = True
                supporting_evidence.append(f"stub_struct_{tf}")
                supporting_evidence.append(f"stub_liq_{tf}")
                
        # Synthesize Bias
        direction = "BULLISH" if has_structure and has_liquidity else "NEUTRAL"
        
        return BiasNode(
            node_id=f"bias_{uuid.uuid4().hex[:8]}",
            identity=None,
            concept_type=NarrativeNodeType.BIAS,
            concept_name=f"{direction} Bias",
            direction=direction,
            supported_by_structure=has_structure,
            supported_by_liquidity=has_liquidity,
            supported_by_regions=has_regions,
            supporting_evidence_ids=supporting_evidence,
            producer_plugin="ICTPlugin",
            producer_policy="v1.0"
        )
        
    def evaluate_pois(self, mtf_graph: MultiTimeframeEvidenceGraph) -> List[POINode]:
        """
        Identifies generic objective regions and casts them into ICT-relevant POIs (FVGs, OBs).
        """
        pois = []
        
        for tf in self.htf_intervals:
            graph = mtf_graph.timeframe(tf)
            if graph:
                # We would query the objective graph for regions
                # and emit POINodes for the ones ICT cares about.
                pois.append(
                    POINode(
                        node_id=f"poi_{uuid.uuid4().hex[:8]}",
                        identity=None,
                        concept_type=NarrativeNodeType.POI,
                        concept_name=f"HTF FVG ({tf})",
                        poi_type="FVG",
                        is_active=True,
                        supporting_evidence_ids=[f"stub_fvg_evidence_{tf}"],
                        producer_plugin="ICTPlugin",
                        producer_policy="v1.0"
                    )
                )
                
        return pois
