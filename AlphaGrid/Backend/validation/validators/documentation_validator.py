from Backend.validation.validators.abstract_validator import AbstractValidator
from Backend.validation.dtos import ValidationContextDTO, ValidatorResultDTO
import subprocess

class DocumentationValidator(AbstractValidator):
    def run_validation(self, context: ValidationContextDTO) -> ValidatorResultDTO:
        try:
            result = subprocess.run(["python", "Scripts/ci_docs.py"], capture_output=True, text=True, cwd=context.workspace)
            if result.returncode == 0:
                return ValidatorResultDTO(
                    id=self.validator_id, status="PASS", duration_ms=0.0,
                    phase=context.phase, family=context.family, summary="Documentation validated."
                )
            else:
                return ValidatorResultDTO(
                    id=self.validator_id, status="FAIL", duration_ms=0.0,
                    phase=context.phase, family=context.family, summary="ci_docs.py failed.",
                    errors=[result.stdout]
                )
        except Exception as e:
            return ValidatorResultDTO(id=self.validator_id, status="ERROR", duration_ms=0.0, phase=context.phase, family=context.family, errors=[str(e)])
