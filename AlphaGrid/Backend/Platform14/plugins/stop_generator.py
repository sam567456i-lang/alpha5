from typing import Dict, Any
from Backend.Platform14.contracts.dtos import RecommendationDTO
from Backend.Platform14.plugins.base import AbstractGeneratorPlugin

class StructuralStopGenerator(AbstractGeneratorPlugin):
    @property
    def plugin_id(self) -> str:
        return "plugin_stop_generator"

    def generate(self, dto: RecommendationDTO, policy: Dict[str, Any]) -> None:
        buffer_pct = policy.get("buffer_percent", 0.05)
        
        if dto.entry_price:
            dto.direction = dto.evaluated_opportunity.opportunity.direction
            if dto.direction == "LONG":
                dto.stop_loss = dto.entry_price * (1 - buffer_pct)
            else:
                dto.stop_loss = dto.entry_price * (1 + buffer_pct)
            dto.execution_notes.append("Stop loss calculated using structural buffer.")

class ATRStopGenerator(AbstractGeneratorPlugin):
    @property
    def plugin_id(self) -> str:
        return "plugin_atr_stop"

    def generate(self, dto: RecommendationDTO, policy: Dict[str, Any]) -> None:
        dto.execution_notes.append("ATR Stop calculation scaffolded.")
