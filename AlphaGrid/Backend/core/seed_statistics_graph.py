import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from Backend.core.capability_knowledge_graph import CapabilityKnowledgeGraph, CapabilityNode, CRL
from Backend.core.graph_visualizer import KnowledgeGraphVisualizer
from Backend.foundation.base_registry import BaseRegistry
from Backend.foundation.global_registry import get_global_registry

def seed_statistics():
    graph = CapabilityKnowledgeGraph()
    
    # 1. Distribution Engine
    graph.add_node(CapabilityNode(
        identity="P10-STAT-DIST-001",
        domain="Foundation",
        platform="Platform10",
        program="Pipeline",
        family="Statistics",
        engine="DistributionEngine",
        evidence_produced=["DistributionEvidence"],
        evidence_consumed=["PriceEvidence"],
        dependencies=["P10-DATA-PRICE-001"],
        consumers=["P10-STAT-NORM-001", "P10-STAT-VOL-001", "P10-TREND-001"],
        crl=CRL.CRL3_PROTOTYPE,
        version="1.0.0",
        adr="ADR-STAT-001",
        owner="core_team"
    ))

    # 2. Rolling Engine
    graph.add_node(CapabilityNode(
        identity="P10-STAT-ROLL-001",
        domain="Foundation",
        platform="Platform10",
        program="Pipeline",
        family="Statistics",
        engine="RollingEngine",
        evidence_produced=["RollingStatisticsEvidence"],
        evidence_consumed=["PriceEvidence"],
        dependencies=["P10-DATA-PRICE-001"],
        consumers=["P10-STAT-NORM-001", "P10-TREND-001", "P10-LIQ-001"],
        crl=CRL.CRL3_PROTOTYPE,
        version="1.0.0",
        adr="ADR-STAT-001",
        owner="core_team"
    ))

    # 3. Volatility Engine
    graph.add_node(CapabilityNode(
        identity="P10-STAT-VOL-001",
        domain="Foundation",
        platform="Platform10",
        program="Pipeline",
        family="Statistics",
        engine="VolatilityEngine",
        evidence_produced=["VolatilityEvidence"],
        evidence_consumed=["PriceEvidence"],
        dependencies=["P10-DATA-PRICE-001"],
        consumers=["P10-TREND-001", "P10-STRUCT-001", "P10-LIQ-001"],
        crl=CRL.CRL3_PROTOTYPE,
        version="1.0.0",
        adr="ADR-STAT-001",
        owner="core_team"
    ))

    # 4. Normalization Engine
    graph.add_node(CapabilityNode(
        identity="P10-STAT-NORM-001",
        domain="Foundation",
        platform="Platform10",
        program="Pipeline",
        family="Statistics",
        engine="NormalizationEngine",
        evidence_produced=["NormalizationEvidence"],
        evidence_consumed=["PriceEvidence", "DistributionEvidence", "RollingStatisticsEvidence"],
        dependencies=["P10-DATA-PRICE-001", "P10-STAT-DIST-001", "P10-STAT-ROLL-001"],
        consumers=["P12-DECISION-001"],
        crl=CRL.CRL3_PROTOTYPE,
        version="1.0.0",
        adr="ADR-STAT-001",
        owner="core_team"
    ))

    visualizer = KnowledgeGraphVisualizer(graph)
    
    os.makedirs("Docs/Registries", exist_ok=True)
    with open("Docs/Registries/Statistics_Graph.json", "w") as f:
        f.write(visualizer.to_json())
        
    print("Seeded Knowledge Graph and exported Statistics_Graph.json")

if __name__ == "__main__":
    seed_statistics()
