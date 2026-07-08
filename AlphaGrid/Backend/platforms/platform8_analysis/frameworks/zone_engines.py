from typing import List, Dict, Any, Optional
from dataclasses import replace
from Backend.shared_domain.contracts.zones.zone_dtos import ZoneDTO, ZoneGeometryDTO, ZoneLifecycleStatus

class RegistryResolver:
    """Resolves registry configurations for a specific zone type."""
    def __init__(self, registry_data: Dict[str, Any]):
        self.registry = registry_data

    def get_policy(self, zone_type: str, policy_name: str) -> Dict[str, Any]:
        return self.registry.get("zone_types", {}).get(zone_type, {}).get(policy_name, {})

class OverlapEngine:
    """Handles overlap detection and containment logic."""
    @staticmethod
    def calculate_overlap_percentage(z1: ZoneDTO, z2: ZoneDTO) -> float:
        overlap_top = min(z1.geometry.upper_price, z2.geometry.upper_price)
        overlap_bottom = max(z1.geometry.lower_price, z2.geometry.lower_price)
        
        if overlap_bottom >= overlap_top:
            return 0.0
            
        overlap_range = overlap_top - overlap_bottom
        z1_range = z1.geometry.upper_price - z1.geometry.lower_price
        
        if z1_range == 0:
            return 0.0
            
        return overlap_range / z1_range

class MergeEngine:
    """Handles merging multiple zones into a single zone."""
    def __init__(self, registry_resolver: RegistryResolver):
        self.resolver = registry_resolver

    def attempt_merge(self, z1: ZoneDTO, z2: ZoneDTO) -> Optional[ZoneDTO]:
        policy = self.resolver.get_policy(z1.identity.zone_type, "merge_policy")
        if not policy.get("allow_merge", False):
            return None
            
        new_top = max(z1.geometry.upper_price, z2.geometry.upper_price)
        new_bottom = min(z1.geometry.lower_price, z2.geometry.lower_price)
        new_geometry = replace(z1.geometry, upper_price=new_top, lower_price=new_bottom)
        
        return replace(
            z1, 
            geometry=new_geometry,
            lineage_ids=z1.lineage_ids + z2.lineage_ids + [z2.identity.zone_id]
        )

class SplitEngine:
    """Handles splitting a large zone into multiple sub-zones (e.g. after mitigation)."""
    def __init__(self, registry_resolver: RegistryResolver):
        self.resolver = registry_resolver
        
    def attempt_split(self, zone: ZoneDTO, split_price: float) -> List[ZoneDTO]:
        policy = self.resolver.get_policy(zone.identity.zone_type, "split_policy")
        if not policy.get("allow_split", False):
            return [zone]
            
        if split_price >= zone.geometry.upper_price or split_price <= zone.geometry.lower_price:
            return [zone]
            
        geom_upper = replace(zone.geometry, lower_price=split_price)
        geom_lower = replace(zone.geometry, upper_price=split_price)
        z_upper = replace(zone, geometry=geom_upper)
        z_lower = replace(zone, geometry=geom_lower)
        return [z_upper, z_lower]

class LifecycleEngine:
    """Handles state machine transitions for zones."""
    def __init__(self, registry_resolver: RegistryResolver):
        self.lifecycle_config = registry_resolver.registry.get("lifecycle", {})
        
    def transition(self, zone: ZoneDTO, event: str) -> ZoneDTO:
        current_state = zone.status.value
        transitions = self.lifecycle_config.get("states", {}).get(current_state, {})
        
        if event in transitions:
            next_state_str = transitions[event]["next"]
            next_state = ZoneLifecycleStatus(next_state_str)
            return replace(zone, status=next_state)
            
        return zone

class FreshnessEngine:
    """Handles aging and freshness decay for zones."""
    def __init__(self, registry_resolver: RegistryResolver):
        self.resolver = registry_resolver
        
    def decay(self, zone: ZoneDTO, current_bar_index: int) -> ZoneDTO:
        policy = self.resolver.get_policy(zone.identity.zone_type, "aging_policy")
        decay_rate = policy.get("decay_rate", 0.0)
        
        new_freshness = max(0.0, zone.freshness - decay_rate)
        return replace(zone, freshness=new_freshness)

class ConfidenceEngine:
    """Handles dynamic confidence updates for zones."""
    def __init__(self, registry_resolver: RegistryResolver):
        self.resolver = registry_resolver
        
    def update_confidence(self, zone: ZoneDTO, confluence_factors: List[float]) -> ZoneDTO:
        new_strength = min(1.0, zone.strength + sum(confluence_factors))
        return replace(zone, strength=new_strength)

class ReplayEngine:
    """Handles stream reconstruction of historical zone events."""
    def __init__(self, registry_resolver: RegistryResolver):
        self.resolver = registry_resolver
        
    def reconstruct_from_stream(self, events: List[Any]) -> List[ZoneDTO]:
        pass
