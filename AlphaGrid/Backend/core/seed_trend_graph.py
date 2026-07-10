import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from Backend.core.capability_knowledge_graph import CapabilityKnowledgeGraph, CapabilityNode, CRL
from Backend.core.graph_visualizer import KnowledgeGraphVisualizer

def seed_trend():
    graph = CapabilityKnowledgeGraph()
    
    # Direction Engine
    graph.add_node(CapabilityNode(
        identity="P10-TREND-DIR-001",
        domain="Trend",
        platform="Platform10",
        program="Pipeline",
        family="Trend",
        engine="DirectionEngine",
        evidence_produced=["TrendDirectionEvidence"],
        evidence_consumed=["RollingStatisticsEvidence", "VolatilityEvidence"],
        dependencies=["P10-STAT-ROLL-001", "P10-STAT-VOL-001"],
        consumers=["P10-TREND-STATE-001", "P10-SWING-001"],
        crl=CRL.CRL3_PROTOTYPE,
        version="1.0.0",
        adr="ADR-TREND-001",
        owner="core_team"
    ))

    # Strength Engine
    graph.add_node(CapabilityNode(
        identity="P10-TREND-STR-001",
        domain="Trend",
        platform="Platform10",
        program="Pipeline",
        family="Trend",
        engine="StrengthEngine",
        evidence_produced=["TrendStrengthEvidence"],
        evidence_consumed=["PriceEvidence", "VolatilityEvidence"],
        dependencies=["P10-DATA-PRICE-001", "P10-STAT-VOL-001"],
        consumers=["P10-TREND-STATE-001", "P10-LIQ-001"],
        crl=CRL.CRL3_PROTOTYPE,
        version="1.0.0",
        adr="ADR-TREND-001",
        owner="core_team"
    ))

    # Geometry Engine
    graph.add_node(CapabilityNode(
        identity="P10-TREND-GEO-001",
        domain="Trend",
        platform="Platform10",
        program="Pipeline",
        family="Trend",
        engine="GeometryEngine",
        evidence_produced=["TrendSlopeEvidence", "TrendAccelerationEvidence"],
        evidence_consumed=["RollingStatisticsEvidence"],
        dependencies=["P10-STAT-ROLL-001"],
        consumers=["P10-TREND-STATE-001", "P11-PROFILES"],
        crl=CRL.CRL3_PROTOTYPE,
        version="1.0.0",
        adr="ADR-TREND-001",
        owner="core_team"
    ))

    # State Engine
    graph.add_node(CapabilityNode(
        identity="P10-TREND-STATE-001",
        domain="Trend",
        platform="Platform10",
        program="Pipeline",
        family="Trend",
        engine="StateEngine",
        evidence_produced=["TrendStateEvidence"],
        evidence_consumed=["TrendDirectionEvidence", "TrendStrengthEvidence", "TrendSlopeEvidence", "VolatilityEvidence"],
        dependencies=["P10-TREND-DIR-001", "P10-TREND-STR-001", "P10-TREND-GEO-001", "P10-STAT-VOL-001"],
        consumers=["P10-SWING-001", "P10-STRUCT-001"],
        crl=CRL.CRL3_PROTOTYPE,
        version="1.0.0",
        adr="ADR-TREND-001",
        owner="core_team"
    ))

    # Persistence Engine
    graph.add_node(CapabilityNode(
        identity="P10-TREND-PER-001",
        domain="Trend",
        platform="Platform10",
        program="Pipeline",
        family="Trend",
        engine="PersistenceEngine",
        evidence_produced=["TrendPersistenceEvidence"],
        evidence_consumed=["TrendDirectionEvidence", "TimeEvidence"],
        dependencies=["P10-TREND-DIR-001", "P10-DATA-TIME-001"],
        consumers=["P11-PROFILES"],
        crl=CRL.CRL3_PROTOTYPE,
        version="1.0.0",
        adr="ADR-TREND-001",
        owner="core_team"
    ))

    visualizer = KnowledgeGraphVisualizer(graph)
    
    os.makedirs("Docs/Registries", exist_ok=True)
    with open("Docs/Registries/Trend_Graph.json", "w") as f:
        f.write(visualizer.to_json())
        
    print("Seeded Knowledge Graph and exported Trend_Graph.json")

if __name__ == "__main__":
    seed_trend()
