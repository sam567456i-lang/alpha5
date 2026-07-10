from abc import ABC, abstractmethod
from typing import Dict

class BaseMathematicalBaseline(ABC):
    """The interface for a strategy that sets the minimum hurdle rate for a Methodology."""
    
    @abstractmethod
    def generate_metrics(self) -> Dict[str, float]:
        pass

class BuyAndHold(BaseMathematicalBaseline):
    def generate_metrics(self) -> Dict[str, float]:
        return {"win_rate": 0.52, "sharpe_ratio": 1.1, "max_drawdown": 0.25}
        
class CoinFlipRandom(BaseMathematicalBaseline):
    def generate_metrics(self) -> Dict[str, float]:
        return {"win_rate": 0.50, "sharpe_ratio": 0.0, "max_drawdown": 0.85}
        
class SMACrossover(BaseMathematicalBaseline):
    def generate_metrics(self) -> Dict[str, float]:
        return {"win_rate": 0.45, "sharpe_ratio": 0.8, "max_drawdown": 0.18}

class SimpleMomentum(BaseMathematicalBaseline):
    def generate_metrics(self) -> Dict[str, float]:
        return {"win_rate": 0.48, "sharpe_ratio": 0.9, "max_drawdown": 0.20}

class SimpleMeanReversion(BaseMathematicalBaseline):
    def generate_metrics(self) -> Dict[str, float]:
        return {"win_rate": 0.65, "sharpe_ratio": 1.2, "max_drawdown": 0.35}
