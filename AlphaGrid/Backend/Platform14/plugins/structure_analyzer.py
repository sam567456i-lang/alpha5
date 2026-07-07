from typing import Dict, Any
from Backend.Platform14.contracts.dtos import RecommendationDTO
from Backend.Platform14.plugins.base import AbstractAnalyzerPlugin

class TradeStructureAnalyzer(AbstractAnalyzerPlugin):
    @property
    def plugin_id(self) -> str:
        return "plugin_structure_analyzer"

    def analyze(self, dto: RecommendationDTO, policy: Dict[str, Any]) -> None:
        if dto.entry_price and dto.stop_loss and dto.take_profit_targets:
            risk = abs(dto.entry_price - dto.stop_loss)
            reward = abs(dto.take_profit_targets[0] - dto.entry_price)
            if risk > 0:
                dto.risk_reward_ratio = reward / risk
                dto.execution_notes.append(f"Trade structure analyzed. Base R:R is {dto.risk_reward_ratio:.2f}")
