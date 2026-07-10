from typing import Dict, Any, List
from Backend.core.methodology.evaluators.base_evaluator import BaseEvaluator
from Backend.core.methodology.dto.base_candidate import SessionCandidate
from Backend.core.methodology.dto.base_evaluation import BaseEvaluation, PassedEvaluation

class SessionEvaluator(BaseEvaluator):
    """
    Evaluates SessionCandidates against methodology-specific session policies (e.g. Killzones).
    Migrated from legacy ICT session mapping.
    """
    def __init__(self, policy_config: Dict[str, Any] = None):
        self.policy_config = policy_config or {}
        
        # Defaults matching legacy KillzonePolicy and SilverBulletPolicy
        self.london_windows = self.policy_config.get("london_windows", ["02:00-05:00"])
        self.ny_am_windows = self.policy_config.get("new_york_am_windows", ["08:30-12:00"])
        self.ny_pm_windows = self.policy_config.get("new_york_pm_windows", ["13:30-16:00"])
        self.asian_windows = self.policy_config.get("asian_windows", ["20:00-00:00"])
        self.sb_windows = self.policy_config.get("silver_bullet_windows", ["10:00-11:00", "14:00-15:00"])

    def evaluate(self, candidate: SessionCandidate, context: Dict[str, Any]) -> BaseEvaluation:
        active_windows = candidate.active_windows
        
        active_sessions = []
        is_sb = False
        
        # Legacy mapping logic
        if any(w in self.london_windows for w in active_windows):
            active_sessions.append("LONDON_KILLZONE")
        if any(w in self.ny_am_windows for w in active_windows):
            active_sessions.append("NEW_YORK_AM_KILLZONE")
        if any(w in self.ny_pm_windows for w in active_windows):
            active_sessions.append("NEW_YORK_PM_KILLZONE")
        if any(w in self.asian_windows for w in active_windows):
            active_sessions.append("ASIAN_KILLZONE")
            
        if any(w in self.sb_windows for w in active_windows):
            is_sb = True
            
        return PassedEvaluation(
            evaluator_id="SessionEvaluator",
            reasons=["Session mapped successfully"],
            metadata={
                "active_sessions": active_sessions,
                "is_silver_bullet": is_sb
            }
        )
