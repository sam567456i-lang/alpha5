from typing import Dict, Any
from Backend.Platform14.contracts.dtos import RecommendationDTO
from Backend.Platform14.plugins.base import AbstractGeneratorPlugin

class ZoneEntryGenerator(AbstractGeneratorPlugin):
    @property
    def plugin_id(self) -> str:
        return "plugin_entry_generator"

    def generate(self, dto: RecommendationDTO, policy: Dict[str, Any]) -> None:
        buffer_pct = policy.get("buffer_percent", 0.0)
        base_price = 100.0 # Mock extraction from context
        
        dto.entry_price = base_price
        dto.entry_zone_min = base_price * (1 - buffer_pct)
        dto.entry_zone_max = base_price * (1 + buffer_pct)
        dto.execution_notes.append("Entry zone calculated using percentage buffer.")

class TWAPEntryGenerator(AbstractGeneratorPlugin):
    @property
    def plugin_id(self) -> str:
        return "plugin_twap_entry"

    def generate(self, dto: RecommendationDTO, policy: Dict[str, Any]) -> None:
        dto.execution_notes.append("TWAP entry calculation scaffolded.")
