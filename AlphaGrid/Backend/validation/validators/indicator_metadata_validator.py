import time
from Backend.validation.validators.abstract_validator import AbstractValidator
from Backend.validation.dtos import ValidationContextDTO, ValidatorResultDTO
from Backend.indicator_engine.registry import IndicatorRegistry

class IndicatorMetadataValidator(AbstractValidator):
    def run_validation(self, context: ValidationContextDTO) -> ValidatorResultDTO:
        start = time.perf_counter()
        errors = []
        
        required_keys = ["formula", "inputs", "outputs", "warmup", "complexity", "streaming", "deterministic"]
        
        for name, registration in IndicatorRegistry.get_all().items():
            engine = registration["engine"]
            if not hasattr(engine, "metadata"):
                errors.append(f"Indicator '{name}' is missing static metadata.")
                continue
                
            metadata = engine.metadata
            for key in required_keys:
                if key not in metadata:
                    errors.append(f"Indicator '{name}' metadata is missing required key '{key}'.")
                    
        duration_ms = (time.perf_counter() - start) * 1000.0
        
        if errors:
            return ValidatorResultDTO(
                id=self.validator_id, status="FAIL", duration_ms=duration_ms,
                phase=context.phase, family=context.family,
                errors=errors, summary=f"Failed metadata validation for {len(errors)} engines."
            )
            
        return ValidatorResultDTO(
            id=self.validator_id, status="PASS", duration_ms=duration_ms,
            phase=context.phase, family=context.family,
            summary="All registered indicator engines have complete static metadata."
        )
