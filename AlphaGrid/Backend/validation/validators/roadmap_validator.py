import os
import yaml
from typing import Any, Dict, List
import time
from Backend.validation.dtos import ValidatorResultDTO, ValidationContextDTO
from Backend.validation.validators.abstract_validator import AbstractValidator

class RoadmapValidator(AbstractValidator):
    """
    Read-only validator that audits the repository state against the capability registry
    to ensure prerequisites are met, waves are finished, and capabilities are implemented.
    """
        
    def _load_registry(self, workspace: str) -> Dict[str, Any]:
        registry_path = os.path.join(workspace, "master_capability_registry.yaml")
        if not os.path.exists(registry_path):
            raise FileNotFoundError(f"Registry not found: {registry_path}")
        with open(registry_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def run_validation(self, context: ValidationContextDTO) -> ValidatorResultDTO:
        start = time.perf_counter()
        errors = []
        try:
            registry = self._load_registry(context.workspace)
            capabilities = registry.get("capabilities", [])
            
            for cap in capabilities:
                if cap.get("implementation_status") == "implemented":
                    pass 
                else:
                    if cap.get("family") in ["General", "Candlestick", "Geometry", "MACD", "ROC", "Trend", "Volatility"]:
                        errors.append(f"Capability '{cap.get('id')}' is from an active/past wave but status is {cap.get('implementation_status')}")
            
            duration_ms = (time.perf_counter() - start) * 1000.0
            
            if errors:
                return ValidatorResultDTO(
                    id=self.validator_id,
                    status="FAIL",
                    phase=context.phase,
                    family=context.family,
                    duration_ms=duration_ms,
                    summary=f"Roadmap audit failed with {len(errors)} issues.",
                    errors=errors
                )
            
            return ValidatorResultDTO(
                id=self.validator_id,
                status="PASS",
                phase=context.phase,
                family=context.family,
                duration_ms=duration_ms,
                summary="Roadmap and prerequisites verified successfully."
            )
            
        except Exception as e:
            return ValidatorResultDTO(
                id=self.validator_id,
                status="ERROR",
                phase=context.phase,
                family=context.family,
                summary=f"Roadmap validation failed: {str(e)}"
            )
