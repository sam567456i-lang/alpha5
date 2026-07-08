from enum import Enum
from dataclasses import dataclass

class ExecutionMode(Enum):
    REPLAY = "REPLAY"
    STREAMING = "STREAMING"
    SNAPSHOT = "SNAPSHOT"
    INCREMENTAL = "INCREMENTAL"
    HISTORICAL = "HISTORICAL"
    SIMULATION = "SIMULATION"

@dataclass(frozen=True)
class ExecutionModeDTO:
    """
    Defines the universal runtime execution mode for Platform 10 and beyond.
    Methodologies consume this to understand how they should evaluate state.
    """
    mode: ExecutionMode
    description: str
