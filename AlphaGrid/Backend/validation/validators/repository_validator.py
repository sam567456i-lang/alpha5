import subprocess
from Backend.validation.validators.abstract_validator import AbstractValidator
from Backend.validation.dtos import ValidationContextDTO, ValidatorResultDTO
import os

class RepositoryValidator(AbstractValidator):
    def run_validation(self, context: ValidationContextDTO) -> ValidatorResultDTO:
        # We run pytest
        cmd = ["python", "-m", "pytest", "Tests/"]
        # Actually just run the simplest version for now so we don't wait forever, or run tests that might fail
        # For AlphaGrid we want this to be real. Let's run pytest but only on Tests/
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=context.workspace)
            if result.returncode == 0:
                return ValidatorResultDTO(
                    id=self.validator_id,
                    status="PASS",
                    duration_ms=0.0,
                    phase=context.phase,
                    family=context.family,
                    summary="All unit tests passed."
                )
            else:
                return ValidatorResultDTO(
                    id=self.validator_id,
                    status="FAIL",
                    duration_ms=0.0,
                    phase=context.phase,
                    family=context.family,
                    errors=[result.stdout[-1000:]],
                    summary="Pytest failed."
                )
        except Exception as e:
            return ValidatorResultDTO(
                id=self.validator_id,
                status="ERROR",
                duration_ms=0.0,
                phase=context.phase,
                family=context.family,
                errors=[str(e)],
                summary="Failed to execute pytest."
            )
