from typing import Dict, Any, List

class MethodologyStateMachine:
    """
    Governs the lifecycle of a Methodology assessment.
    Transitions are strictly enforced based on registry-defined rules.
    """
    def __init__(self, config: Dict[str, Any]):
        self.state = config.get("initial_state", "PENDING_EVALUATION")
        self.terminal_states = config.get("terminal_states", [])
        self.transitions = config.get("transitions", [])

    def transition(self, target_state: str, context_checks: Dict[str, bool]) -> bool:
        if self.state in self.terminal_states:
            return False # Cannot transition out of terminal state
            
        for t in self.transitions:
            if t["from"] == self.state and t["to"] == target_state:
                guard = t.get("guard")
                if guard and not context_checks.get(guard, False):
                    return False
                self.state = target_state
                return True
        return False
        
    def get_state(self) -> str:
        return self.state
