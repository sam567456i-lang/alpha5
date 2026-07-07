import os
import importlib
import inspect
from typing import Dict, Any, Type, List
from Backend.Platform10.contracts.interfaces import IMethodologyPlugin

class PluginLoader:
    """Platform 10 Plugin Loader & Registry Validator"""
    
    def __init__(self, registry_caps: List[Dict[str, Any]]):
        self.registry_caps = {cap["id"]: cap for cap in registry_caps if cap.get("entity_type") == "capability"}
        self.loaded_plugins: Dict[str, IMethodologyPlugin] = {}
        
    def discover_and_load(self, plugins_dir: str):
        """Scans the plugins directory and dynamic-loads valid IMethodologyPlugin classes."""
        for root, _, files in os.walk(plugins_dir):
            for file in files:
                if file.endswith(".py") and not file.startswith("__"):
                    module_name = file[:-3]
                    # We assume plugins are in Backend.Platform10.plugins
                    full_module_name = f"Backend.Platform10.plugins.{module_name}"
                    try:
                        module = importlib.import_module(full_module_name)
                        for name, obj in inspect.getmembers(module):
                            if inspect.isclass(obj) and issubclass(obj, IMethodologyPlugin) and obj is not IMethodologyPlugin:
                                plugin_instance = obj()
                                # 1. Registry Validation & Versioning Match
                                self._validate_and_register(plugin_instance)
                    except Exception as e:
                        print(f"[WARN] Failed to load plugin {full_module_name}: {e}")

    def _validate_and_register(self, plugin: IMethodologyPlugin):
        """Cross-references the discovered plugin with the Project OS master registry."""
        cap_id = plugin.methodology_id
        if cap_id not in self.registry_caps:
            print(f"[ERROR] Plugin {cap_id} is not registered in the Master Registry. Rejecting.")
            return
            
        cap_meta = self.registry_caps[cap_id]
        
        # Capability Versioning Match
        reg_version = cap_meta.get("version", "1.0.0")
        if plugin.version != reg_version:
            print(f"[ERROR] Plugin {cap_id} version mismatch! Code={plugin.version}, Registry={reg_version}")
            return
            
        # Lifecycle Check
        if cap_meta.get("lifecycle_status") in ["disabled", "frozen", "deprecated"]:
            print(f"[INFO] Skipping plugin {cap_id}: Lifecycle status is {cap_meta.get('lifecycle_status')}")
            return
            
        self.loaded_plugins[cap_id] = plugin
        print(f"[INFO] Successfully loaded and validated plugin: {cap_id} v{plugin.version}")
        
    def get_plugin(self, cap_id: str) -> IMethodologyPlugin:
        return self.loaded_plugins.get(cap_id)
        
    def get_all_plugins(self) -> List[IMethodologyPlugin]:
        return list(self.loaded_plugins.values())
