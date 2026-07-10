from enum import Enum

class AssetCertificationState(Enum):
    DRAFT = "DRAFT"
    REVIEWED = "REVIEWED"
    APPROVED = "APPROVED"
    REGRESSION_LOCKED = "REGRESSION_LOCKED"
    DEPRECATED = "DEPRECATED"

class AssetCertificationManager:
    """State machine preventing uncertified assets from entering the simulation engine."""
    
    @staticmethod
    def assert_can_use_in_research(state: AssetCertificationState):
        if state in [AssetCertificationState.DRAFT, AssetCertificationState.REVIEWED]:
            raise ValueError(f"Cannot run research on unapproved asset (State: {state})")
        if state == AssetCertificationState.DEPRECATED:
            raise ValueError("Asset is deprecated and unsafe for research.")
            
    @staticmethod
    def assert_can_use_in_regression(state: AssetCertificationState):
        if state != AssetCertificationState.REGRESSION_LOCKED:
            raise ValueError("Only REGRESSION_LOCKED assets can be used in CI/CD pipeline tests.")
