from typing import List, Dict, Set
from Backend.validation.validation_registry import ValidationRegistry
from Backend.validation.dtos import ValidationContextDTO, ValidatorResultDTO
import graphlib

class ValidationRunner:
    def __init__(self, registry: ValidationRegistry):
        self.registry = registry

    def _build_execution_plan(self, profile: str) -> List[str]:
        # 1. Get all validator IDs for this profile
        validators_to_run = self.registry.resolve_profile(profile)
        
        # 2. Build dependency graph just for the active validators
        graph = {}
        for vid in validators_to_run:
            config = self.registry.get_validator_config(vid)
            # Only track dependencies that are actually IN this profile run
            deps = [d for d in config.get('dependencies', []) if d in validators_to_run]
            graph[vid] = set(deps)
            
        # 3. Topologically sort
        ts = graphlib.TopologicalSorter(graph)
        return list(ts.static_order())

    def execute(self, profile: str, context: ValidationContextDTO):
        import time
        import os
        import json
        from Backend.validation.dtos import ValidationEvent
        
        execution_plan = self._build_execution_plan(profile)
        
        yield ValidationEvent(event_type="VALIDATION_STARTED", message=f"Profile {profile}")
        
        passed_validators = set()
        failed_blockers = set()
        
        validators_dir = os.path.join(context.evidence_directory, "validators")
        os.makedirs(validators_dir, exist_ok=True)
        
        total = len(execution_plan)
        for i, vid in enumerate(execution_plan):
            yield ValidationEvent(event_type="VALIDATOR_STARTED", validator_id=vid, progress_pct=(i/total)*100)
            config = self.registry.get_validator_config(vid)
            
            # Check dependencies
            deps = config.get('dependencies', [])
            blocked_by = [d for d in deps if d in failed_blockers]
            
            result = None
            if blocked_by:
                result = ValidatorResultDTO(
                    id=vid,
                    status="SKIPPED",
                    reason=f"Blocked by {blocked_by}",
                    duration_ms=0.0,
                    phase=context.phase,
                    family=context.family,
                    evidence_id=f"EV-{context.phase}-{vid}",
                    summary=f"Skipped due to failed blocking dependencies."
                )
                if config.get('blocking', False):
                    failed_blockers.add(vid)
            else:
                # Run validator
                start_time = time.perf_counter()
                validator = self.registry.instantiate_validator(vid)
                try:
                    result = validator.execute(context)
                    result.evidence_id = f"EV-{context.phase}-{vid}"
                except Exception as e:
                    result = ValidatorResultDTO(
                        id=vid,
                        status="ERROR",
                        reason=str(e),
                        duration_ms=0.0,
                        phase=context.phase,
                        family=context.family,
                        evidence_id=f"EV-{context.phase}-{vid}",
                        errors=[str(e)]
                    )
                end_time = time.perf_counter()
                result.duration_ms = (end_time - start_time) * 1000
                
                if result.status == "PASS":
                    passed_validators.add(vid)
                elif result.status in ["FAIL", "ERROR"] and config.get('blocking', False):
                    failed_blockers.add(vid)
                    
            # Incremental save
            with open(os.path.join(validators_dir, f"{vid}.json"), "w") as f:
                json.dump(result.to_dict(), f, indent=4)
                
            yield ValidationEvent(event_type="VALIDATOR_FINISHED", validator_id=vid, result=result, progress_pct=((i+1)/total)*100)
            
        yield ValidationEvent(event_type="VALIDATION_FINISHED", message="Finished")
