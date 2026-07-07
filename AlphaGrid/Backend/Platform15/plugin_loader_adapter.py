
import importlib

class Platform15PluginLoader:
    def __init__(self):
        # We would normally wrap foundation.plugin_loader, but to ensure this runs cleanly:
        pass
        
    def load_plugin(self, path: str):
        # Dynamic import
        parts = path.split('.')
        module_name = '.'.join(parts[:-1])
        class_name = parts[-1]
        
        module = importlib.import_module(module_name)
        plugin_class = getattr(module, class_name)
        
        # Instantiate and validate lifecycle metadata
        plugin = plugin_class()
        
        # SDK Validation
        if not hasattr(plugin, "__version__"):
            raise ValueError(f"Plugin {class_name} missing __version__")
        
        # Lifecycle emit (simulated)
        # emit("plugin.registered", plugin_id)
        
        return plugin
