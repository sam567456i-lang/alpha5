import os
import json
import time
import hashlib
from Backend.validation.validators.abstract_validator import AbstractValidator
from Backend.validation.dtos import ValidationContextDTO, ValidatorResultDTO

class DatasetValidator(AbstractValidator):
    def run_validation(self, context: ValidationContextDTO) -> ValidatorResultDTO:
        start = time.perf_counter()
        
        manifest_path = os.path.join(context.workspace, "Datasets", "dataset_manifest.json")
        golden_path = os.path.join(context.workspace, "Datasets", "golden", "reference.parquet")
        
        if not os.path.exists(manifest_path) or not os.path.exists(golden_path):
            return ValidatorResultDTO(
                id=self.validator_id, status="SKIPPED", reason="Missing Datasets or manifest.",
                phase=context.phase, family=context.family
            )
            
        with open(manifest_path, "r") as f:
            manifest = json.load(f)
            
        expected_checksum = manifest.get("checksums", {}).get("golden_reference.parquet")
        
        with open(golden_path, "rb") as f:
            actual_checksum = hashlib.sha256(f.read()).hexdigest()
            
        errors = []
        if expected_checksum != actual_checksum:
            errors.append(f"Checksum mismatch for reference.parquet. Expected {expected_checksum}, got {actual_checksum}")
            
        duration_ms = (time.perf_counter() - start) * 1000.0
        
        if errors:
            return ValidatorResultDTO(
                id=self.validator_id, status="FAIL", duration_ms=duration_ms,
                phase=context.phase, family=context.family,
                errors=errors,
                summary="Dataset governance failure: Checksum mismatch."
            )
            
        return ValidatorResultDTO(
            id=self.validator_id, status="PASS", duration_ms=duration_ms,
            phase=context.phase, family=context.family,
            summary=f"Dataset {manifest['dataset_id']} v{manifest['version']} successfully verified."
        )
