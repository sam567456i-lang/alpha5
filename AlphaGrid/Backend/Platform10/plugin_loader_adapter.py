import importlib

class Platform10PluginLoader:
    def __init__(self):
        # We wrap foundation.plugin_loader conceptually
        pass
        
    def load_plugin(self, path: str, expected_wave: int = None):
        parts = path.split('.')
        module_name = '.'.join(parts[:-1])
        class_name = parts[-1]
        
        module = importlib.import_module(module_name)
        plugin_class = getattr(module, class_name)
        plugin = plugin_class()
        
        # New SDK checks (only enforce on Wave 2 or higher)
        if expected_wave and expected_wave >= 2:
            if not hasattr(plugin, "__version__"):
                raise ValueError(f"Wave {expected_wave} Plugin {class_name} missing __version__ (Plugin SDK violation)")
                
        return plugin