import yaml
import os

class ZoneRegistryCertification:
    """Certifies that all Zone Framework registries meet the Wave 3 specifications."""
    def __init__(self, registry_dir: str):
        self.registry_dir = registry_dir
        
    def certify(self):
        errors = []
        files = {
            "zone": "zone_registry.yaml",
            "state_machine": "zone_state_machine_registry.yaml",
            "capability": "zone_capability_registry.yaml",
            "spatial": "spatial_relationship_registry.yaml"
        }
        
        for key, filename in files.items():
            path = os.path.join(self.registry_dir, filename)
            if not os.path.exists(path):
                errors.append(f"Missing {filename}")
                continue
            with open(path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                if not data:
                    errors.append(f"Empty {filename}")
                    continue
                if "version" not in data or "schema" not in data["version"]:
                    errors.append(f"{filename} missing schema version")

        # Specific checks on zone_registry.yaml
        zone_path = os.path.join(self.registry_dir, "zone_registry.yaml")
        if os.path.exists(zone_path):
            with open(zone_path, 'r', encoding='utf-8') as f:
                zone_data = yaml.safe_load(f)
                version_data = zone_data.get("version", {})
                if "adr_reference" not in version_data:
                    errors.append("zone_registry.yaml missing adr_reference")
                
                zone_types = zone_data.get("zone_types", {})
                for zt, config in zone_types.items():
                    if "performance_budget" not in config:
                        errors.append(f"{zt} missing performance_budget")
                    if "compatibility_policy" not in config:
                        errors.append(f"{zt} missing compatibility_policy")
                    if "feature_flag" not in config:
                        errors.append(f"{zt} missing feature_flag")
                    if "required_inputs" not in config:
                        errors.append(f"{zt} missing required_inputs")
                    if "fingerprint_fields" not in config:
                        errors.append(f"{zt} missing fingerprint_fields")

        if errors:
            print("Certification Failed!")
            for e in errors:
                print(f" - {e}")
            exit(1)
        else:
            print("Zone Registry Certified")
            print("Version: 1.0")
            print("Frozen: true")

if __name__ == "__main__":
    registry_dir = os.path.join(os.path.dirname(__file__), "..", "..", "Docs", "Governance", "registry")
    certifier = ZoneRegistryCertification(registry_dir)
    certifier.certify()
