import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from Backend.core.capability_knowledge_graph import CapabilityKnowledgeGraph, CapabilityNode, CRL
from Backend.core.graph_visualizer import KnowledgeGraphVisualizer

def seed_swing():
    graph = CapabilityKnowledgeGraph()
    
    graph.add_node(CapabilityNode(
        identity="P10-SWING-PIVOT-001",
        domain="Primitives",
        platform="Platform10",
        program="Pipeline",
        family="Swing",
        engine="PivotEngine",
        evidence_produced=["PivotEvidence"],
        evidence_consumed=["PriceEvidence", "StatisticsEvidence"],
        dependencies=["P10-DATA-PRICE-001", "P10-STAT-VOL-001"],
        consumers=["P10-SWING-PERSIST-001"],
        crl=CRL.CRL3_PROTOTYPE,
        version="1.0.0",
        adr="ADR-SWING-001",
        owner="core_team"
    ))

    graph.add_node(CapabilityNode(
        identity="P10-SWING-PERSIST-001",
        domain="Primitives",
        platform="Platform10",
        program="Pipeline",
        family="Swing",
        engine="PersistenceEngine",
        evidence_produced=["PivotLifecycleEvidence"],
        evidence_consumed=["PivotEvidence"],
        dependencies=["P10-SWING-PIVOT-001"],
        consumers=["P10-SWING-CLASS-001", "P10-SWING-REL-001"],
        crl=CRL.CRL3_PROTOTYPE,
        version="1.0.0",
        adr="ADR-SWING-001",
        owner="core_team"
    ))
    
    graph.add_node(CapabilityNode(
        identity="P10-SWING-CLASS-001",
        domain="Primitives",
        platform="Platform10",
        program="Pipeline",
        family="Swing",
        engine="ClassificationEngine",
        evidence_produced=["SwingClassificationEvidence"],
        evidence_consumed=["PivotLifecycleEvidence"],
        dependencies=["P10-SWING-PERSIST-001"],
        consumers=["P10-SWING-HIER-001"],
        crl=CRL.CRL3_PROTOTYPE,
        version="1.0.0",
        adr="ADR-SWING-001",
        owner="core_team"
    ))

    graph.add_node(CapabilityNode(
        identity="P10-SWING-REL-001",
        domain="Primitives",
        platform="Platform10",
        program="Pipeline",
        family="Swing",
        engine="RelationshipEngine",
        evidence_produced=["SwingRelationshipEvidence"],
        evidence_consumed=["PivotLifecycleEvidence"],
        dependencies=["P10-SWING-PERSIST-001"],
        consumers=["P10-SWING-HIER-001", "P10-STRUCT-001", "P10-LIQ-001"],
        crl=CRL.CRL3_PROTOTYPE,
        version="1.0.0",
        adr="ADR-SWING-001",
        owner="core_team"
    ))

    graph.add_node(CapabilityNode(
        identity="P10-SWING-HIER-001",
        domain="Primitives",
        platform="Platform10",
        program="Pipeline",
        family="Swing",
        engine="HierarchyEngine",
        evidence_produced=["SwingHierarchyEvidence"],
        evidence_consumed=["SwingClassificationEvidence", "SwingRelationshipEvidence"],
        dependencies=["P10-SWING-CLASS-001", "P10-SWING-REL-001"],
        consumers=["P10-STRUCT-001", "P11-PROFILES"],
        crl=CRL.CRL3_PROTOTYPE,
        version="1.0.0",
        adr="ADR-SWING-001",
        owner="core_team"
    ))

    graph.add_node(CapabilityNode(
        identity="P10-SWING-QUAL-001",
        domain="Primitives",
        platform="Platform10",
        program="Pipeline",
        family="Swing",
        engine="QualityEngine",
        evidence_produced=["SwingQualityEvidence"],
        evidence_consumed=["SwingHierarchyEvidence", "StatisticsEvidence", "PriceEvidence"],
        dependencies=["P10-SWING-HIER-001", "P10-STAT-VOL-001"],
        consumers=["P11-PROFILES", "P12-DECISION"],
        crl=CRL.CRL3_PROTOTYPE,
        version="1.0.0",
        adr="ADR-SWING-001",
        owner="core_team"
    ))

    visualizer = KnowledgeGraphVisualizer(graph)
    
    os.makedirs("Docs/Registries", exist_ok=True)
    with open("Docs/Registries/Swing_Graph.json", "w") as f:
        f.write(visualizer.to_json())
        
    print("Seeded Knowledge Graph and exported Swing_Graph.json")

if __name__ == "__main__":
    seed_swing()
