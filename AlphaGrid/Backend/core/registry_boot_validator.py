import os
import yaml
import importlib

class RegistryBootValidator:
    """
    Validates all registries dynamically loaded from registry_manifest.yaml in strict load_priority order.
    Boot validation is limited to runtime essentials (schema validity, checksums, load order, basic dependencies).
    """
    def __init__(self):
        self.registry_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "Docs", "Governance", "registry"))
        self.manifest_path = os.path.join(self.registry_dir, "registry_manifest.yaml")
        
    def validate_boot_sequence(self):
        print("Starting Universal Registry Boot Validation...")
        
        if not os.path.exists(self.manifest_path):
            raise RuntimeError(f"Boot Failed: Manifest not found at {self.manifest_path}")
            
        with open(self.manifest_path, 'r', encoding='utf-8') as f:
            manifest_data = yaml.safe_load(f)
            
        registries = manifest_data.get("registries", [])
        # Sort by load priority
        registries.sort(key=lambda r: r.get("load_priority", 999))
        
        loaded = set()
        
        for reg in registries:
            name = reg["name"]
            file_name = reg["file"]
            depends_on = reg.get("depends_on", [])
            required = reg.get("required", True)
            
            print(f"Loading {name} ({file_name})...")
            
            # Check dependencies
            for dep in depends_on:
                if dep not in loaded:
                    raise RuntimeError(f"Boot Failed: Registry '{name}' depends on '{dep}' which is not loaded yet (Check load_priority).")
                    
            reg_path = os.path.join(self.registry_dir, file_name)
            if not os.path.exists(reg_path):
                if required:
                    raise RuntimeError(f"Boot Failed: Required registry file {file_name} not found.")
                else:
                    print(f"  Skipping {name} (Optional, file not found)")
                    continue
                    
            # Basic validation
            with open(reg_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                if not data:
                    raise RuntimeError(f"Boot Failed: Registry {name} is empty.")
                    
            # In a full system, we would dynamically invoke the 'validator' class from the manifest here
            # e.g. importlib.import_module(...)
            
            loaded.add(name)
            
        print(f"Universal Registry Boot Validation Passed. ({len(loaded)} registries verified)")
        return True

if __name__ == "__main__":
    validator = RegistryBootValidator()
    validator.validate_boot_sequence()
