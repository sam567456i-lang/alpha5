import pytest
from Backend.core.engine.symbol_identity import SymbolIdentity
from Backend.core.engine.market_universe import MarketUniverse
from Backend.core.analytical_rules.capabilities.evidence_graph import EvidenceGraph
from Backend.core.engine.time_domain import TimeDomain
from Backend.core.engine.symbol_relationship_graph import SymbolRelationshipGraph
from Backend.core.engine.cross_market_analytics_engine import CrossMarketAnalyticsEngine
from Backend.core.engine.regime_engine import RegimeEngine
from Backend.core.engine.event_context_engine import EventContextEngine
from Backend.core.engine.cross_market_comparison_engine import CrossMarketComparisonEngine
from Backend.core.methodology.divergence_policy import DivergencePolicy
from Backend.core.methodology.ict.policies.smt_policy import ICTSMTPolicy

def test_cross_market_infrastructure():
    # 1. Setup Universe & Identity
    es_identity = SymbolIdentity(id="ES", exchange="CME", venue="", currency="USD", contract="FUT", tick_size=0.25, point_value=50, asset_class="INDEX", timezone="EST", trading_calendar="CME", session_template="ETH", roll_schedule="QUARTERLY", precision=2)
    nq_identity = SymbolIdentity(id="NQ", exchange="CME", venue="", currency="USD", contract="FUT", tick_size=0.25, point_value=20, asset_class="INDEX", timezone="EST", trading_calendar="CME", session_template="ETH", roll_schedule="QUARTERLY", precision=2)
    
    universe = MarketUniverse()
    universe.register_symbol(es_identity, EvidenceGraph())
    universe.register_symbol(nq_identity, EvidenceGraph())
    
    # 2. Time Domain & Validity
    time_domain = TimeDomain()
    quality = time_domain.evaluate_data_quality("ES", 0.0, 100.0)
    assert quality.validity_status_flags == "PRISTINE"
    
    # 3. Objective Relationships
    graph = SymbolRelationshipGraph()
    graph.add_edge("ES", "NQ", "INDEX_CORRELATED", 0.95, 1.0)
    
    rel_engine = CrossMarketAnalyticsEngine(graph)
    evidence = rel_engine.compute_relationships("ES")
    
    assert len(evidence) == 2 # Correlation + LeadLag
    assert evidence[0].correlation_coefficient == 0.85 # 0.85 * 1.0
    
    # 4. Context Evidence
    regime_engine = RegimeEngine()
    regimes = regime_engine.compute_regimes("ES")
    assert regimes[0].trend_type == "BULLISH"
    
    event_engine = EventContextEngine()
    events = event_engine.get_upcoming_events(["ES", "NQ"])
    assert events[0].event_name == "FOMC Statement"
    
    # 5. Objective Comparison
    comp_engine = CrossMarketComparisonEngine(graph)
    comparisons = comp_engine.compare_group("US_INDICES")
    
    assert len(comparisons) == 1
    assert comparisons[0].comparison_type == "STRUCTURAL"
    assert comparisons[0].results["ES"] == "HIGHER_HIGH"
    assert comparisons[0].time_alignment == "PRISTINE" # Provenance check
    
    # 6. Divergence Policy
    div_policy = DivergencePolicy()
    div_node = div_policy.evaluate(comparisons[0], "ES", "NQ")
    
    assert div_node is not None
    assert div_node.divergence_type == "HIGHER_HIGH_VS_LOWER_HIGH"
    
    # 7. SMT Policy Application
    smt_policy = ICTSMTPolicy()
    smt_narrative = smt_policy.evaluate(div_node)
    
    assert smt_narrative is not None
    assert smt_narrative.concept_name == "ICT SMT Divergence"
    assert smt_narrative.primary_symbol == "ES"
    assert smt_narrative.diverging_symbol == "NQ"
    assert smt_narrative.bias_indication == "BULLISH"
