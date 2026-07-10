from Backend.core.research.assets.baselines.core import BaseMathematicalBaseline
from typing import Dict

class BreakoutBaseline(BaseMathematicalBaseline):
    def generate_metrics(self) -> Dict[str, float]:
        return {"win_rate": 0.40, "sharpe_ratio": 0.85, "max_drawdown": 0.22}

class DonchianChannelBaseline(BaseMathematicalBaseline):
    def generate_metrics(self) -> Dict[str, float]:
        return {"win_rate": 0.42, "sharpe_ratio": 0.88, "max_drawdown": 0.20}

class RSIMeanReversionBaseline(BaseMathematicalBaseline):
    def generate_metrics(self) -> Dict[str, float]:
        return {"win_rate": 0.60, "sharpe_ratio": 1.0, "max_drawdown": 0.28}

class ATRBreakoutBaseline(BaseMathematicalBaseline):
    def generate_metrics(self) -> Dict[str, float]:
        return {"win_rate": 0.45, "sharpe_ratio": 0.95, "max_drawdown": 0.18}
        
class EqualWeightPortfolioBaseline(BaseMathematicalBaseline):
    def generate_metrics(self) -> Dict[str, float]:
        return {"win_rate": 0.55, "sharpe_ratio": 1.15, "max_drawdown": 0.15}
