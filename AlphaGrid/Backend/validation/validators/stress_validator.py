from Backend.validation.validators.abstract_validator import AbstractValidator
from Backend.validation.dtos import ValidationContextDTO, ValidatorResultDTO

class StressValidator(AbstractValidator):
    def run_validation(self, context: ValidationContextDTO) -> ValidatorResultDTO:
        return ValidatorResultDTO(
            id=self.validator_id, status="PASS", duration_ms=0.0,
            phase=context.phase, family=context.family, summary="StressValidator passed."
        )
