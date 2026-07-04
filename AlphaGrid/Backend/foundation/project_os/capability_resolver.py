from Backend.foundation.project_os.scanner import RepositoryState
from typing import Dict, Any

class CapabilityResolver:
    """Resolves true capability status from physical repository evidence."""
    
    def __init__(self, state: RepositoryState):
        self.state = state

    def resolve(self, capability_name: str) -> Dict[str, Any]:
        """
        Determines the 15-gate DoD status for a capability.
        """
        # Normalize name for file matching
        safe_name = capability_name.lower().replace(" ", "_").replace("/", "_")
        
        # Evidence checks
        math_impl_exists = any(safe_name in f for f in self.state.python_files if "Backend\\math" in f or "Backend/math" in f)
        engine_impl_exists = any(safe_name in f for f in self.state.python_files if "Backend\\indicator_engine" in f or "Backend/indicator_engine" in f)
        
        test_exists = any(safe_name in f for f in self.state.python_files if "Tests" in f)
        
        implemented = math_impl_exists or engine_impl_exists
        
        status = {
            "Capability": capability_name,
            "Implemented": implemented,
            "Implementation Evidence": "File found" if implemented else "No python file found",
            "Unit Tested": test_exists,
            "Test Evidence": "Test file found" if test_exists else "No test file found",
            "Validated": False, # Advanced validation logic
            "Dashboard Compatible": False, # Requires dashboard schema lookup
            "AI Compatible": False # Requires metadata lookup
        }
        
        return status
