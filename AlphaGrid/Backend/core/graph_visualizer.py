import json
from Backend.core.capability_knowledge_graph import CapabilityKnowledgeGraph

class KnowledgeGraphVisualizer:
    """Generates varied structural outputs for the Capability Knowledge Graph."""
    def __init__(self, graph: CapabilityKnowledgeGraph):
        self.graph = graph

    def to_json(self) -> str:
        nodes = []
        for n in self.graph.get_all_nodes():
            nodes.append({
                "identity": n.identity,
                "domain": n.domain,
                "family": n.family,
                "engine": n.engine,
                "dependencies": n.dependencies,
                "evidence_produced": n.evidence_produced,
                "crl": n.crl.name
            })
        return json.dumps({"nodes": nodes}, indent=2)

    def to_mermaid(self) -> str:
        lines = ["graph TD;"]
        for n in self.graph.get_all_nodes():
            lines.append(f'    {n.identity}["{n.domain}: {n.engine}"]')
            for dep in n.dependencies:
                lines.append(f"    {dep} --> {n.identity}")
        return "\n".join(lines)

    def to_dot(self) -> str:
        lines = ["digraph CapabilityGraph {", "  rankdir=LR;"]
        for n in self.graph.get_all_nodes():
            lines.append(f'  "{n.identity}" [label="{n.domain}\\n{n.engine}"];')
            for dep in n.dependencies:
                lines.append(f'  "{dep}" -> "{n.identity}";')
        lines.append("}")
        return "\n".join(lines)
