from typing import Dict, Any
from Backend.core.interfaces.execution_mode_dto import ExecutionMode

class MethodologyPolicyEngine:
    """
    Enforces execution policies (timeouts, retry logic, aggregation, streaming vs replay).
    Separates the "rules" of execution from the orchestrating runtime.
    """
    def __init__(self, policy_config: Dict[str, Any]):
        self.config = policy_config
        
    def check_timeout(self, elapsed_ms: int) -> bool:
        timeout = self.config.get("timeout_ms", 100)
        return elapsed_ms > timeout
        
    def is_mode_supported(self, mode: ExecutionMode) -> bool:
        if mode == ExecutionMode.STREAMING:
            return self.config.get("streaming_support", False)
        if mode == ExecutionMode.REPLAY:
            return self.config.get("replay_support", False)
        return True
