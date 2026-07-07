import importlib
import inspect
import glob
import os
import yaml
from abc import ABC, abstractmethod
from typing import Dict, List, Type, Any
from Backend.core.state import BaseState
from Shared.dtos.execution_context import ExecutionContext

class AnalysisPlugin(ABC):
    """
    Base class for all Platform 8 Analysis plugins.
    A plugin represents a complete family of analysis (e.g., Geometry, Price Action).
    """
    
    @property
    @abstractmethod
    def family_name(self) -> str:
        pass

    @property
    @abstractmethod
    def supported_markets(self) -> List[str]:
        pass
        
    @abstractmethod
    def register_states(self) -> Dict[str, Type[BaseState]]:
        """
        Returns a dictionary mapping capability_id to the specific State class it produces.
        """
        pass
        
    @abstractmethod
    def execute(self, inputs: Dict[str, Any], context: ExecutionContext) -> Dict[str, BaseState]:
        """
        Execute the analysis family logic and return the newly generated states.
        inputs must contain all required upstream states.
        """
        pass

class DependencyResolver:
    """
    Resolves plugin execution order based on State dependency graphs.
    Enforces the Platform Purity Rule by ensuring no plugin consumes downstream data.
    Now strictly uses the Governance YAML registry (Registry-driven architecture) 
    instead of hardcoding or inferring from python classes.
    """
    def __init__(self, registry_path: str):
        self.registry_path = registry_path
        
    def resolve_execution_order(self, plugins: List[AnalysisPlugin]) -> List[AnalysisPlugin]:
        """
        Perform a topological sort based on the states each plugin produces and consumes,
        as defined in the authoritative YAML registry.
        """
        # Load registry
        if not os.path.exists(self.registry_path):
            # Fallback to independent if no registry, though in production this should fail
            return plugins
            
        with open(self.registry_path, "r", encoding="utf-8") as f:
            registry_data = yaml.safe_load(f) or {}
            
        entries = registry_data.get("entries", [])
        cap_dict = {entry["id"]: entry for entry in entries}
        
        # Build dependency graph
        plugin_produces = {}
        plugin_consumes = {}
        
        for p in plugins:
            produces = set()
            consumes = set()
            for cap_id, _ in p.register_states().items():
                produces.add(cap_id)
                # Read consumes from registry instead of python class
                if cap_id in cap_dict:
                    cap_deps = cap_dict[cap_id].get("dependencies", [])
                    consumes.update([dep["id"] for dep in cap_deps if "id" in dep])
            
            plugin_produces[p.family_name] = produces
            plugin_consumes[p.family_name] = consumes
            
        # Topological Sort (Kahn's Algorithm)
        in_degree = {p.family_name: 0 for p in plugins}
        adj = {p.family_name: [] for p in plugins}
        
        for p1 in plugins:
            for p2 in plugins:
                if p1 == p2:
                    continue
                # If p2 consumes what p1 produces, p1 -> p2
                if plugin_consumes[p2.family_name].intersection(plugin_produces[p1.family_name]):
                    adj[p1.family_name].append(p2.family_name)
                    in_degree[p2.family_name] += 1
                    
        queue = [p.family_name for p in plugins if in_degree[p.family_name] == 0]
        sorted_family_names = []
        
        while queue:
            curr = queue.pop(0)
            sorted_family_names.append(curr)
            for neighbor in adj[curr]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
                    
        if len(sorted_family_names) != len(plugins):
            raise RuntimeError("Circular dependency detected in Platform 8 Analysis Plugins based on Registry!")
            
        # Map back to objects
        plugin_map = {p.family_name: p for p in plugins}
        return [plugin_map[name] for name in sorted_family_names]

class PluginLoader:
    """
    Dynamically loads all plugins in the Platform 8 Analysis Framework.
    """
    def __init__(self, plugin_dir: str):
        self.plugin_dir = plugin_dir
        self.plugins: Dict[str, AnalysisPlugin] = {}
        
    def discover_and_load(self) -> None:
        """
        Dynamically imports plugin modules from the plugin_dir.
        """
        search_pattern = os.path.join(self.plugin_dir, "*_plugin.py")
        for file_path in glob.glob(search_pattern):
            module_name = os.path.basename(file_path)[:-3]
            # Construct absolute module path assuming plugin_dir is absolute
            # We can use importlib.util for absolute path loading
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Find classes inheriting from AnalysisPlugin
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if issubclass(obj, AnalysisPlugin) and obj is not AnalysisPlugin:
                        # Instantiate the plugin
                        plugin_instance = obj()
                        self.register_plugin(plugin_instance)
        
    def register_plugin(self, plugin: AnalysisPlugin) -> None:
        self.plugins[plugin.family_name] = plugin
        
    def get_all_plugins(self) -> List[AnalysisPlugin]:
        return list(self.plugins.values())
