from typing import Dict, Any
from Backend.Platform14.contracts.dtos import RecommendationDTO, RecommendationState
from Backend.Platform14.plugins.base import AbstractAnalyzerPlugin

class PrePublishValidator(AbstractAnalyzerPlugin):
    @property
    def plugin_id(self) -> str:
        return "plugin_pre_publish_validator"

    def analyze(self, dto: RecommendationDTO, policy: Dict[str, Any]) -> None:
        """Validates that the recommendation is mathematically sound before publishing."""
        dto.validation_errors.clear()
        
        if not dto.entry_price or not dto.stop_loss:
            dto.validation_errors.append("Missing entry or stop price.")
            return

        if dto.direction == "LONG" and dto.entry_price <= dto.stop_loss:
            dto.validation_errors.append("LONG entry price must be > stop loss.")
            
        if dto.direction == "SHORT" and dto.entry_price >= dto.stop_loss:
            dto.validation_errors.append("SHORT entry price must be < stop loss.")

        min_rr = policy.get("min_rr", 1.0)
        if dto.risk_reward_ratio < min_rr:
            dto.validation_errors.append(f"Risk/Reward {dto.risk_reward_ratio:.2f} is below minimum {min_rr}.")
