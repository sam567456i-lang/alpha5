import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from Backend.core.capability_knowledge_graph import CapabilityKnowledgeGraph, CapabilityNode, CRL
from Backend.core.graph_visualizer import KnowledgeGraphVisualizer

def seed_range():
    graph = CapabilityKnowledgeGraph()
    
    graph.add_node(CapabilityNode(
        identity="P10-RANGE-BOUND-001",
        domain="Primitives",
        platform="Platform10",
        program="Pipeline",
        family="Range",
        engine="BoundaryEngine",
        evidence_produced=["RangeBoundaryEvidence"],
        evidence_consumed=["SwingRelationshipEvidence", "PivotLifecycleEvidence", "PriceEvidence"],
        dependencies=["P10-SWING-REL-001", "P10-SWING-PERSIST-001", "P10-DATA-PRICE-001"],
        consumers=["P10-RANGE-GEOM-001", "P10-RANGE-HIER-001", "P10-LIQ-001", "P10-STRUCT-001"],
        crl=CRL.CRL3_PROTOTYPE,
        version="1.0.0",
        adr="ADR-RANGE-001",
        owner="core_team"
    ))

    graph.add_node(CapabilityNode(
        identity="P10-RANGE-TEMP-001",
        domain="Primitives",
        platform="Platform10",
        program="Pipeline",
        family="Range",
        engine="TemporalEngine",
        evidence_produced=["TemporalRangeEvidence"],
        evidence_consumed=["TimeEvidence", "PriceEvidence"],
        dependencies=["P10-DATA-TIME-001", "P10-DATA-PRICE-001"],
        consumers=["P10-RANGE-GEOM-001", "P11-PROFILES"],
        crl=CRL.CRL3_PROTOTYPE,
        version="1.0.0",
        adr="ADR-RANGE-001",
        owner="core_team"
    ))

    graph.add_node(CapabilityNode(
        identity="P10-RANGE-GEOM-001",
        domain="Primitives",
        platform="Platform10",
        program="Pipeline",
        family="Range",
        engine="GeometryEngine",
        evidence_produced=["RangeGeometryEvidence"],
        evidence_consumed=["RangeBoundaryEvidence", "TemporalRangeEvidence"],
        dependencies=["P10-RANGE-BOUND-001", "P10-RANGE-TEMP-001"],
        consumers=["P10-RANGE-STATE-001"],
        crl=CRL.CRL3_PROTOTYPE,
        version="1.0.0",
        adr="ADR-RANGE-001",
        owner="core_team"
    ))

    graph.add_node(CapabilityNode(
        identity="P10-RANGE-STATE-001",
        domain="Primitives",
        platform="Platform10",
        program="Pipeline",
        family="Range",
        engine="StateEngine",
        evidence_produced=["RangeStateEvidence"],
        evidence_consumed=["RangeGeometryEvidence", "StatisticsEvidence"],
        dependencies=["P10-RANGE-GEOM-001", "P10-STAT-VOL-001"],
        consumers=["P11-PROFILES", "P10-IMBAL-001"],
        crl=CRL.CRL3_PROTOTYPE,
        version="1.0.0",
        adr="ADR-RANGE-001",
        owner="core_team"
    ))

    graph.add_node(CapabilityNode(
        identity="P10-RANGE-HIER-001",
        domain="Primitives",
        platform="Platform10",
        program="Pipeline",
        family="Range",
        engine="HierarchyEngine",
        evidence_produced=["RangeHierarchyEvidence"],
        evidence_consumed=["RangeBoundaryEvidence"],
        dependencies=["P10-RANGE-BOUND-001"],
        consumers=["P11-PROFILES"],
        crl=CRL.CRL3_PROTOTYPE,
        version="1.0.0",
        adr="ADR-RANGE-001",
        owner="core_team"
    ))

    visualizer = KnowledgeGraphVisualizer(graph)
    
    os.makedirs("Docs/Registries", exist_ok=True)
    with open("Docs/Registries/Range_Graph.json", "w") as f:
        f.write(visualizer.to_json())
        
    print("Seeded Knowledge Graph and exported Range_Graph.json")

if __name__ == "__main__":
    seed_range()
