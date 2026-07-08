import os
import yaml

class ZoneRegistryValidator:
    """Validates Platform 8 Zone registries."""
    def __init__(self):
        self.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "Docs", "Governance", "registry"))

    def validate_all(self) -> bool:
        """Validates all Platform 8 core registries."""
        try:
            zone_cap_path = os.path.join(self.base_dir, "zone_capability_registry.yaml")
            with open(zone_cap_path, 'r', encoding='utf-8') as f:
                cap_reg = yaml.safe_load(f).get("capabilities", {})
                
            zone_path = os.path.join(self.base_dir, "zone_registry.yaml")
            with open(zone_path, 'r', encoding='utf-8') as f:
                zone_reg = yaml.safe_load(f).get("zone_types", {})
                
            # Perform a basic check to ensure registries are properly populated
            if not cap_reg or not zone_reg:
                print("Zone or Capability registry is empty!")
                return False
                
            return True
        except Exception as e:
            print(f"ZoneRegistryValidator failed: {e}")
            return False
