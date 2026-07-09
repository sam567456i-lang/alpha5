from typing import Callable, Any, Dict
from dataclasses import dataclass
import threading

@dataclass
class PluginCapabilities:
    """Explicit contracts for what a plugin is allowed to do."""
    can_read_evidence_graph: bool = True
    can_emit_narrative_graph: bool = True
    can_modify_evidence_graph: bool = False
    can_access_scheduler: bool = False
    can_access_configuration: bool = False

class SandboxFault(Exception):
    pass

class PluginSandbox:
    """
    Executes third-party or internal plugins in isolated environments
    based on their trust level (0=Internal, 1=Trusted, 2=Untrusted/Process, 3=Remote/RPC).
    """
    def __init__(self, level: int = 0, capabilities: PluginCapabilities = None):
        self.level = level
        self.capabilities = capabilities or PluginCapabilities()
        
    def execute(self, plugin_callable: Callable, *args, **kwargs) -> Any:
        if self.level == 0:
            return self._execute_level_0(plugin_callable, *args, **kwargs)
        elif self.level == 1:
            return self._execute_level_1(plugin_callable, *args, **kwargs)
        else:
            raise NotImplementedError(f"Sandbox level {self.level} not yet implemented.")
            
    def _execute_level_0(self, plugin_callable: Callable, *args, **kwargs) -> Any:
        """Internal plugin: Basic try/except boundary."""
        try:
            return plugin_callable(*args, **kwargs)
        except Exception as e:
            raise SandboxFault(f"Plugin crashed: {str(e)}")
            
    def _execute_level_1(self, plugin_callable: Callable, *args, **kwargs) -> Any:
        """Trusted plugin: Thread boundary."""
        result = None
        error = None
        
        def wrapper():
            nonlocal result, error
            try:
                result = plugin_callable(*args, **kwargs)
            except Exception as e:
                error = e
                
        t = threading.Thread(target=wrapper)
        t.start()
        t.join(timeout=30.0) # 30s budget
        
        if t.is_alive():
            raise SandboxFault("Plugin execution timed out")
        if error:
            raise SandboxFault(f"Plugin crashed in thread: {str(error)}")
            
        return result
