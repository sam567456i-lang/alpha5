from dataclasses import dataclass, field
from typing import List

@dataclass
class SessionSetupConfiguration:
    name: str
    required_objective_windows: List[str] = field(default_factory=list)
    requires_displacement: bool = True

@dataclass
class ICTSessionSetupPolicy:
    """
    Evaluates SessionSetupCandidateNodes against ICT time-based models.
    """
    configurations: List[SessionSetupConfiguration] = field(default_factory=lambda: [
        SessionSetupConfiguration(
            name="SILVER_BULLET_AM",
            required_objective_windows=["10:00-11:00"],
            requires_displacement=True
        ),
        SessionSetupConfiguration(
            name="SILVER_BULLET_PM",
            required_objective_windows=["14:00-15:00"],
            requires_displacement=True
        ),
        SessionSetupConfiguration(
            name="LONDON_KILLZONE",
            required_objective_windows=["02:00-05:00"],
            requires_displacement=True
        )
    ])
