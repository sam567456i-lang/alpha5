from typing import Dict, Any
from Backend.Platform14.contracts.dtos import RecommendationDTO
from Backend.Platform14.plugins.base import AbstractGeneratorPlugin

class FixedRRTargetGenerator(AbstractGeneratorPlugin):
    @property
    def plugin_id(self) -> str:
        return "plugin_target_generator"

    def generate(self, dto: RecommendationDTO, policy: Dict[str, Any]) -> None:
        target_rr = policy.get("target_rr", 2.0)
        
        if dto.entry_price and dto.stop_loss:
            risk = abs(dto.entry_price - dto.stop_loss)
            reward = risk * target_rr
            
            if dto.direction == "LONG":
                target = dto.entry_price + reward
            else:
                target = dto.entry_price - reward
                
            dto.take_profit_targets = [target]
            dto.execution_notes.append(f"Fixed target generated using {target_rr} R:R.")

class LiquidityTargetGenerator(AbstractGeneratorPlugin):
    @property
    def plugin_id(self) -> str:
        return "plugin_liquidity_target"

    def generate(self, dto: RecommendationDTO, policy: Dict[str, Any]) -> None:
        dto.execution_notes.append("Liquidity Target calculation scaffolded.")
