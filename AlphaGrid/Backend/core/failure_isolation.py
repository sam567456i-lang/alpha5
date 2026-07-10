import traceback
from typing import Callable, Any, Dict

class FailureIsolationWrapper:
    """Isolates plugin failures from crashing the main Platform 10 runtime."""
    
    @staticmethod
    def execute_safely(func: Callable, *args, **kwargs) -> Dict[str, Any]:
        try:
            result = func(*args, **kwargs)
            return {"success": True, "result": result, "error": None}
        except Exception as e:
            error_details = {
                "type": type(e).__name__,
                "message": str(e),
                "traceback": traceback.format_exc()
            }
            return {"success": False, "result": None, "error": error_details}
