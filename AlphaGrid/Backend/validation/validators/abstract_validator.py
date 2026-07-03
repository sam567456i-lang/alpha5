from abc import ABC, abstractmethod
from Backend.validation.dtos import ValidationContextDTO, ValidatorResultDTO
import time

class AbstractValidator(ABC):
    
    def __init__(self, validator_id: str, config: dict):
        self.validator_id = validator_id
        self.config = config
        
    def _is_applicable(self, context: ValidationContextDTO) -> bool:
        min_phase = self.config.get('minimum_phase')
        max_phase = self.config.get('maximum_phase')
        
        # Simple integer extraction (e.g. '10e' -> 10)
        try:
            current_phase_num = int("".join(filter(str.isdigit, context.phase)))
        except ValueError:
            current_phase_num = 0
            
        if min_phase is not None and current_phase_num < min_phase:
            return False
            
        if max_phase is not None and current_phase_num > max_phase:
            return False
            
        return True

    def execute(self, context: ValidationContextDTO) -> ValidatorResultDTO:
        start_time = time.time()
        
        if not self._is_applicable(context):
            return ValidatorResultDTO(
                id=self.validator_id,
                status="SKIPPED",
                duration_ms=(time.time() - start_time) * 1000,
                phase=context.phase,
                family=context.family,
                summary=f"Skipped: Not applicable for phase {context.phase}"
            )
            
        try:
            result = self.run_validation(context)
            result.duration_ms = (time.time() - start_time) * 1000
            return result
        except Exception as e:
            return ValidatorResultDTO(
                id=self.validator_id,
                status="ERROR",
                duration_ms=(time.time() - start_time) * 1000,
                phase=context.phase,
                family=context.family,
                errors=[str(e)],
                summary="Validator crashed unexpectedly."
            )
            
    @abstractmethod
    def run_validation(self, context: ValidationContextDTO) -> ValidatorResultDTO:
        """Core logic to be implemented by child classes."""
        pass
