import os
import ast
import json
import time
from Backend.validation.validators.abstract_validator import AbstractValidator
from Backend.validation.dtos import ValidationContextDTO, ValidatorResultDTO

class ArchitectureDriftValidator(AbstractValidator):
    def run_validation(self, context: ValidationContextDTO) -> ValidatorResultDTO:
        start = time.perf_counter()
        backend_dir = os.path.join(context.workspace, "Backend")
        
        current_graph = {}
        for root, dirs, files in os.walk(backend_dir):
            if "legacy" in dirs:
                dirs.remove("legacy")
            for file in files:
                if file.endswith(".py"):
                    path = os.path.join(root, file)
                    rel_path = os.path.relpath(path, backend_dir).replace(os.sep, '.')[:-3]
                    module_name = f"Backend.{rel_path}"
                    
                    deps = set()
                    try:
                        with open(path, "r", encoding="utf-8") as f:
                            tree = ast.parse(f.read(), filename=path)
                        for node in ast.walk(tree):
                            if isinstance(node, ast.Import):
                                for alias in node.names:
                                    deps.add(alias.name.split('.')[0])
                            elif isinstance(node, ast.ImportFrom):
                                if node.module:
                                    deps.add(node.module.split('.')[0])
                    except Exception:
                        pass
                    current_graph[module_name] = sorted(list(deps))
                    
        # Write current graph to TEMP
        temp_dir = os.path.join(context.workspace, "Docs", "Evidence", "2026", "EV-TEMP", "validators")
        os.makedirs(temp_dir, exist_ok=True)
        out_path = os.path.join(temp_dir, "dependency_graph.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(current_graph, f, indent=4)
            
        errors = []
        
        # New strict architectural intent rules
        for mod, current_deps in current_graph.items():
            # Features cannot import Math internals directly
            if "Backend.features" in mod and "generator" in mod:
                for dep in current_deps:
                    if dep.startswith("Backend.math"):
                        errors.append(f"Drift Violation: Feature Generator '{mod}' imports Math Core '{dep}'. Generators must delegate to Indicator Engine.")
            
            # Indicator Engine must not leak DTOs directly (it returns FinancialIndicatorResult)
            if "Backend.indicator_engine" in mod:
                for dep in current_deps:
                    if "Backend.dtos" in dep:
                        errors.append(f"Drift Violation: Engine '{mod}' imports DTOs '{dep}'. DTOs belong in the Feature Layer.")
            
            # Concepts cannot perform math
            if "Backend.research.concepts" in mod:
                for dep in current_deps:
                    if dep.startswith("Backend.math"):
                        errors.append(f"Drift Violation: Concept '{mod}' imports Math '{dep}'. Concepts cannot calculate.")
                        
        # Check API Freeze Manifest
        import hashlib
        api_manifest_path = os.path.join(context.workspace, "Docs", "Governance", "api_freeze_manifest.json")
        if os.path.exists(api_manifest_path):
            with open(api_manifest_path, "r", encoding="utf-8") as f:
                api_manifest = json.load(f).get("locked_apis", {})
            for rel_path, expected_hash in api_manifest.items():
                full_path = os.path.join(context.workspace, os.path.normpath(rel_path))
                if not os.path.exists(full_path):
                    errors.append(f"API Freeze Violation: Locked file missing: {rel_path}")
                else:
                    with open(full_path, "rb") as f:
                        current_hash = hashlib.sha256(f.read()).hexdigest()
                    if current_hash != expected_hash:
                        errors.append(f"API Freeze Violation: Locked API file modified without re-approval: {rel_path}")
                        
        # If there's a reference graph, compare
        if hasattr(context, 'reference_graph_path') and context.reference_graph_path and os.path.exists(context.reference_graph_path):
            with open(context.reference_graph_path, "r", encoding="utf-8") as f:
                prev_graph = json.load(f)
                
            for mod, current_deps in current_graph.items():
                if mod in prev_graph:
                    new_deps = set(current_deps) - set(prev_graph[mod])
                    if new_deps:
                        errors.append(f"Module {mod} introduced new dependencies: {new_deps}")
                        
        duration_ms = (time.perf_counter() - start) * 1000.0
        
        if errors:
            return ValidatorResultDTO(
                id=self.validator_id, status="FAIL", duration_ms=duration_ms,
                phase=context.phase, family=context.family,
                errors=errors,
                summary=f"Architecture drift detected: {len(errors)} violations."
            )
            
        return ValidatorResultDTO(
            id=self.validator_id, status="PASS", duration_ms=duration_ms,
            phase=context.phase, family=context.family,
            summary="No architecture drift detected."
        )
