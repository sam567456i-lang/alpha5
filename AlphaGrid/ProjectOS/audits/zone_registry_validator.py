import yaml
import os

class ZoneRegistryValidator:
    """Audits the spatial zone registry for inconsistencies."""
    def __init__(self, registry_path: str):
        with open(registry_path, 'r', encoding='utf-8') as f:
            self.registry = yaml.safe_load(f)
            
    def validate(self) -> list[str]:
        errors = []
        errors.extend(self._check_schema())
        errors.extend(self._check_unreachable_states())
        errors.extend(self._check_policies())
        errors.extend(self._check_duplicate_priorities())
        errors.extend(self._check_orphans())
        errors.extend(self._check_engine_capabilities())
        return errors

    def _check_schema(self) -> list[str]:
        errors = []
        if "zone_types" not in self.registry:
            errors.append("Missing 'zone_types' in registry.")
        if "lifecycle" not in self.registry:
            errors.append("Missing 'lifecycle' in registry.")
        return errors

    def _check_unreachable_states(self) -> list[str]:
        errors = []
        lifecycle = self.registry.get("lifecycle", {})
        states = lifecycle.get("states", {})
        terminals = lifecycle.get("terminal_states", [])
        
        reachable = set(["PENDING", "DETECTED"])  # Entry points
        for state, transitions in states.items():
            for event, target in transitions.items():
                if isinstance(target, dict) and "next" in target:
                    reachable.add(target["next"])
                    
        for state in states:
            if state not in reachable and state not in terminals:
                errors.append(f"Unreachable state detected: {state}")
                
        return errors
        
    def _check_policies(self) -> list[str]:
        errors = []
        zone_types = self.registry.get("zone_types", {})
        
        for z_type, policies in zone_types.items():
            if "creation_policy" not in policies:
                errors.append(f"Missing creation_policy for {z_type}")
            if "merge_policy" not in policies:
                errors.append(f"Missing merge_policy for {z_type}")
            if "split_policy" not in policies:
                errors.append(f"Missing split_policy for {z_type}")
            if "confidence_policy" not in policies:
                errors.append(f"Missing confidence_policy for {z_type}")
            if "freshness_policy" not in policies:
                errors.append(f"Missing freshness_policy for {z_type}")
            
            vp = policies.get("visualization_policy", {})
            if "presentation_hint" not in vp:
                errors.append(f"Missing presentation_hint in visualization_policy for {z_type}")
        return errors

    def _check_duplicate_priorities(self) -> list[str]:
        errors = []
        priorities = set()
        zone_types = self.registry.get("zone_types", {})
        for z_type, policies in zone_types.items():
            p = policies.get("visualization_policy", {}).get("priority")
            if p is not None:
                if p in priorities:
                    errors.append(f"Duplicate visualization priority found: {p}")
                priorities.add(p)
        return errors

    def _check_orphans(self) -> list[str]:
        errors = []
        zone_types = self.registry.get("zone_types", {})
        for z_type, config in zone_types.items():
            if not config.get("capabilities"):
                errors.append(f"Zone type {z_type} has no declared capabilities (orphan risk).")
        return errors

    def _check_engine_capabilities(self) -> list[str]:
        errors = []
        engines = self.registry.get("engines", [])
        if not engines:
            errors.append("No processing engines defined in registry.")
        return errors

if __name__ == "__main__":
    registry_path = os.path.join(os.path.dirname(__file__), "..", "..", "Docs", "Governance", "registry", "zone_registry.yaml")
    validator = ZoneRegistryValidator(registry_path)
    errors = validator.validate()
    if errors:
        print("Zone Registry Validation Failed:")
        for e in errors:
            print(f" - {e}")
        exit(1)
    else:
        print("Zone Registry Validation Passed.")
