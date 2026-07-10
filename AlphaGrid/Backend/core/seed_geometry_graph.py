import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from Backend.core.capability_knowledge_graph import CapabilityKnowledgeGraph, CapabilityNode, CRL
from Backend.core.graph_visualizer import KnowledgeGraphVisualizer

def seed_geometry():
    graph = CapabilityKnowledgeGraph()
    
    graph.add_node(CapabilityNode(
        identity="P10-GEOM-DIST-001",
        domain="Primitives",
        platform="Platform10",
        program="Pipeline",
        family="Geometry",
        engine="DistanceEngine",
        evidence_produced=["DistanceEvidence"],
        evidence_consumed=["SwingEvidence", "RangeBoundaryEvidence", "TimeEvidence", "PriceEvidence"],
        dependencies=["P10-SWING-PERSIST-001", "P10-RANGE-BOUND-001", "P10-DATA-TIME-001"],
        consumers=["P10-STRUCT-001", "P10-LIQ-OBJ-001"],
        crl=CRL.CRL3_PROTOTYPE,
        version="1.0.0",
        adr="ADR-GEOM-001",
        owner="core_team"
    ))

    graph.add_node(CapabilityNode(
        identity="P10-GEOM-ANGLE-001",
        domain="Primitives",
        platform="Platform10",
        program="Pipeline",
        family="Geometry",
        engine="AngleVectorEngine",
        evidence_produced=["VectorEvidence"],
        evidence_consumed=["SwingEvidence", "TrendEvidence"],
        dependencies=["P10-SWING-PERSIST-001", "P10-TREND-001"],
        consumers=["P10-STRUCT-001", "P11-PROFILES"],
        crl=CRL.CRL3_PROTOTYPE,
        version="1.0.0",
        adr="ADR-GEOM-001",
        owner="core_team"
    ))

    graph.add_node(CapabilityNode(
        identity="P10-GEOM-INTERSECT-001",
        domain="Primitives",
        platform="Platform10",
        program="Pipeline",
        family="Geometry",
        engine="IntersectionEngine",
        evidence_produced=["IntersectionEvidence", "ContainmentEvidence"],
        evidence_consumed=["SwingEvidence", "RangeBoundaryEvidence"],
        dependencies=["P10-SWING-PERSIST-001", "P10-RANGE-BOUND-001"],
        consumers=["P10-LIQ-EVT-001", "P10-STRUCT-EVT-001"],
        crl=CRL.CRL3_PROTOTYPE,
        version="1.0.0",
        adr="ADR-GEOM-001",
        owner="core_team"
    ))

    graph.add_node(CapabilityNode(
        identity="P10-GEOM-PROJ-001",
        domain="Primitives",
        platform="Platform10",
        program="Pipeline",
        family="Geometry",
        engine="ProjectionEngine",
        evidence_produced=["ProjectionEvidence"],
        evidence_consumed=["SwingEvidence", "RangeGeometryEvidence"],
        dependencies=["P10-SWING-PERSIST-001", "P10-RANGE-GEOM-001"],
        consumers=["P11-PROFILES"],
        crl=CRL.CRL3_PROTOTYPE,
        version="1.0.0",
        adr="ADR-GEOM-001",
        owner="core_team"
    ))

    visualizer = KnowledgeGraphVisualizer(graph)
    
    os.makedirs("Docs/Registries", exist_ok=True)
    with open("Docs/Registries/Geometry_Graph.json", "w") as f:
        f.write(visualizer.to_json())
        
    print("Seeded Knowledge Graph and exported Geometry_Graph.json")

if __name__ == "__main__":
    seed_geometry()
