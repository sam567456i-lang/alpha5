import networkx as nx
from typing import List, Dict, Set

class EvidenceDependencyGraph:
    """
    Analyzes dependency chains purely at the evidence level,
    independent of the rules that produce/consume them.
    Supports production views (who produces this) and 
    consumption views (who consumes this).
    """
    def __init__(self):
        self.production_graph = nx.DiGraph() # evidence -> producer_rule
        self.consumption_graph = nx.DiGraph() # evidence -> consumer_rule
        self.evidence_chain = nx.DiGraph() # evidence -> evidence

    def add_production(self, producer_rule: str, produced_evidence: List[str]):
        """Records which rule produces which evidence."""
        for ev in produced_evidence:
            self.production_graph.add_edge(producer_rule, ev)

    def add_consumption(self, consumer_rule: str, consumed_evidence: List[str]):
        """Records which rule consumes which evidence."""
        for ev in consumed_evidence:
            self.consumption_graph.add_edge(ev, consumer_rule)

    def build_evidence_chain(self):
        """Constructs the pure evidence-to-evidence graph based on production/consumption."""
        # if Rule A produces EvX, and Rule B consumes EvX and produces EvY,
        # then EvX -> EvY is an edge in the evidence chain.
        for ev in self.consumption_graph.nodes():
            consumers = list(self.consumption_graph.successors(ev))
            for consumer in consumers:
                if consumer in self.production_graph:
                    produced = list(self.production_graph.successors(consumer))
                    for p_ev in produced:
                        self.evidence_chain.add_edge(ev, p_ev)

    def get_producers(self, evidence: str) -> List[str]:
        if evidence in self.production_graph.nodes():
            return list(self.production_graph.predecessors(evidence))
        return []

    def get_consumers(self, evidence: str) -> List[str]:
        if evidence in self.consumption_graph.nodes():
            return list(self.consumption_graph.successors(evidence))
        return []

    def what_breaks_if_changed(self, evidence: str) -> Set[str]:
        """Returns all downstream rules and evidence impacted by a change."""
        if evidence not in self.evidence_chain:
            return set()
        downstream_evidence = set(nx.descendants(self.evidence_chain, evidence))
        impacted_rules = set()
        
        # Add direct consumers of this evidence
        impacted_rules.update(self.get_consumers(evidence))
        
        # Add consumers of all downstream evidence
        for dev in downstream_evidence:
            impacted_rules.update(self.get_consumers(dev))
            
        return impacted_rules | downstream_evidence
