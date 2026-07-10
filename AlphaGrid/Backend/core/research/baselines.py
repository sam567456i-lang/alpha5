from abc import ABC, abstractmethod
from typing import Dict, Any

class BaselineStrategy(ABC):
    @abstractmethod
    def generate_metrics(self) -> Dict[str, float]:
        pass

class BuyAndHoldBaseline(BaselineStrategy):
    def generate_metrics(self) -> Dict[str, float]:
        return {"win_rate": 0.5, "expectancy": 0.05, "sharpe_ratio": 1.2}

class RandomEntryBaseline(BaselineStrategy):
    def generate_metrics(self) -> Dict[str, float]:
        return {"win_rate": 0.49, "expectancy": -0.01, "sharpe_ratio": -0.1}

class BaselineLibrary:
    def __init__(self):
        self.baselines = {
            "BUY_AND_HOLD": BuyAndHoldBaseline(),
            "RANDOM_ENTRY": RandomEntryBaseline()
        }
        
    def get_baseline_metrics(self, baseline_id: str) -> Dict[str, float]:
        if baseline_id not in self.baselines:
            raise KeyError(f"Baseline {baseline_id} not found.")
        return self.baselines[baseline_id].generate_metrics()
