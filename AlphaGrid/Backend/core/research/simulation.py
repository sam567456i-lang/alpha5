from enum import Enum
from typing import Iterator, Any
from datetime import datetime
from Backend.core.research.dataset_registry import DatasetMetadata

class SimulationMode(Enum):
    REPLAY = "REPLAY"
    STREAMING = "STREAMING"
    PAPER_TRADING = "PAPER_TRADING"
    SYNTHETIC_GENERATOR = "SYNTHETIC_GENERATOR"
    MONTE_CARLO = "MONTE_CARLO"
    SCENARIO_INJECTION = "SCENARIO_INJECTION"

class SimulationEngine:
    """The deterministic engine that routes all historical or live data into the platform."""
    
    def __init__(self, mode: SimulationMode):
        self.mode = mode
        self.current_simulation_time: datetime = datetime.min
        
    def get_time(self) -> datetime:
        """Overrides system time for all downstream components."""
        return self.current_simulation_time
        
    def run_simulation(self, dataset: DatasetMetadata) -> Iterator[Any]:
        """Yields ticks/bars sequentially, updating internal simulated time."""
        # Stub logic for demonstration
        self.current_simulation_time = dataset.start_time
        yield {"event": "SIMULATION_START", "time": self.current_simulation_time}
        # In reality, this yields parsed data structures directly into Platform 10
