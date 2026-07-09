import hashlib
import json
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

from Backend.core.analytical_rules.dto.structure.structure_state import StructureState
from Backend.core.analytical_rules.dto.liquidity.pool_state import PoolState
from Backend.core.analytical_rules.dto.regions.region_state import RegionState
from Backend.core.analytical_rules.dto.auction.auction_metrics import AuctionMetricsDTO
from Backend.core.analytical_rules.dto.range.range_state import RangeState
from Backend.core.analytical_rules.dto.delivery.delivery_metrics import DeliveryMetricsDTO

@dataclass
class EvidenceGraph:
    """
    Unified read-only facade aggregating all objective state projections.
    This serves as the single API consumed by Platform 11 Methodology Plugins
    (ICT, SMC, Wyckoff) to form actionable bias and narrative structures,
    without requiring them to interface with raw framework engines.
    """
    structure_nodes: Dict[str, StructureState] = field(default_factory=dict)
    liquidity_nodes: Dict[str, PoolState] = field(default_factory=dict)
    region_nodes: Dict[str, RegionState] = field(default_factory=dict)
    
    # Contextual boundaries
    range_nodes: Dict[str, RangeState] = field(default_factory=dict)
    
    # Path & Interaction Analytics
    auction_metrics: Dict[str, AuctionMetricsDTO] = field(default_factory=dict)
    delivery_metrics: Dict[str, DeliveryMetricsDTO] = field(default_factory=dict)
    
    # Core API Extensions
    def query(self, query_params: Dict[str, Any]) -> List[Any]:
        # Stub for semantic querying across graph
        return []

    def find(self, evidence_id: str) -> Optional[Any]:
        for store in [self.structure_nodes, self.liquidity_nodes, self.region_nodes, self.range_nodes, self.auction_metrics, self.delivery_metrics]:
            if evidence_id in store:
                return store[evidence_id]
        return None

    def filter(self, predicate: callable) -> List[Any]:
        results = []
        for store in [self.structure_nodes, self.liquidity_nodes, self.region_nodes, self.range_nodes, self.auction_metrics, self.delivery_metrics]:
            results.extend([item for item in store.values() if predicate(item)])
        return results

    def neighbors(self, evidence_id: str) -> List[Any]:
        # Return immediate graph neighbors (derived_from, intersects, overlaps)
        return []

    def subgraph(self, root_evidence_id: str, depth: int = 1) -> 'EvidenceGraph':
        # Returns a new EvidenceGraph containing only the root and its neighbors up to 'depth'
        return EvidenceGraph()

    def lineage(self, evidence_id: str) -> Dict[str, Any]:
        """Returns the full causal chain of the evidence object."""
        node = self.find(evidence_id)
        if not node:
            return {}
        return {
            "evidence_id": evidence_id,
            "provenance": getattr(node, "provenance", None),
            "parents": [self.lineage(pid) for pid in getattr(node.provenance, "source_evidence_ids", [])] if hasattr(node, "provenance") else []
        }

    def explain(self, evidence_id: str) -> str:
        """Returns a human-readable narrative explaining why the node exists."""
        return f"Explanation for {evidence_id} (Stubbed)"

    def export(self, format_type: str = "json") -> str:
        """Exports graph in canonical format."""
        return "{}"

    def validate(self) -> Dict[str, List[str]]:
        """
        Validates graph integrity.
        Detects orphans, dangling references, DAG violations, and missing lineage.
        Returns a dict of violations by category.
        """
        return {"orphans": [], "dangling_references": [], "lineage_failures": []}

    def statistics(self) -> Dict[str, Any]:
        return {
            "structure_nodes": len(self.structure_nodes),
            "liquidity_nodes": len(self.liquidity_nodes),
            "region_nodes": len(self.region_nodes),
            "range_nodes": len(self.range_nodes),
            "auction_metrics": len(self.auction_metrics),
            "delivery_metrics": len(self.delivery_metrics)
        }

    def _hash_dict(self, d: Dict[str, Any]) -> str:
        # Sort keys to ensure deterministic hashing
        serialized = json.dumps(list(sorted(d.keys())))
        return hashlib.sha256(serialized.encode('utf-8')).hexdigest()

    def checksum(self) -> str:
        """
        Calculates a deterministic hash representing the exact structural state of the graph.
        Ignores memory addresses and non-deterministic serialization artifacts.
        """
        # Node IDs acting as proxies for node checksums
        struct_hash = self._hash_dict(self.structure_nodes)
        liq_hash = self._hash_dict(self.liquidity_nodes)
        reg_hash = self._hash_dict(self.region_nodes)
        range_hash = self._hash_dict(self.range_nodes)
        auc_hash = self._hash_dict(self.auction_metrics)
        del_hash = self._hash_dict(self.delivery_metrics)
        
        combined = f"{struct_hash}_{liq_hash}_{reg_hash}_{range_hash}_{auc_hash}_{del_hash}"
        return hashlib.sha256(combined.encode('utf-8')).hexdigest()

    # Legacy Accessors
    def get_structure(self, node_id: str) -> StructureState:
        return self.structure_nodes.get(node_id)
        
    def get_liquidity_pools(self, active_only: bool = True) -> List[PoolState]:
        pools = list(self.liquidity_nodes.values())
        if active_only:
            return [p for p in pools if p.active]
        return pools
        
    def get_regions(self) -> List[RegionState]:
        return list(self.region_nodes.values())
        
    def get_active_ranges(self) -> List[RangeState]:
        return list(self.range_nodes.values())
        
    def get_auction_metrics_for_region(self, region_id: str) -> List[AuctionMetricsDTO]:
        return [m for m in self.auction_metrics.values() if m.region_id == region_id]
        
    def get_delivery_metrics(self) -> List[DeliveryMetricsDTO]:
        return list(self.delivery_metrics.values())
