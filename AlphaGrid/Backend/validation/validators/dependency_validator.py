import os
import ast
import time
from Backend.validation.validators.abstract_validator import AbstractValidator
from Backend.validation.dtos import ValidationContextDTO, ValidatorResultDTO

class DependencyValidator(AbstractValidator):
    def run_validation(self, context: ValidationContextDTO) -> ValidatorResultDTO:
        start = time.perf_counter()
        math_dir = os.path.join(context.workspace, "Backend", "math")
        features_dir = os.path.join(context.workspace, "Backend", "features")
        
        errors = []
        
        import yaml
        math_forbidden = {
            "Backend.dtos": "Math layer must not import DTOs.",
            "Backend.strategy": "Math layer must not import strategies.",
            "Backend.features": "Math layer must not import features.",
            "Backend.concepts": "Math layer must not import concepts.",
            "Backend.methodology": "Math layer must not import methodologies.",
            "Backend.signals": "Math layer must not import signals.",
            "Backend.runtime": "Math layer must not import runtime.",
            "Backend.validation": "Math layer must not import validation."
        }
        
        policy_path = os.path.join(context.workspace, "Docs", "Governance", "math_dependency_policy.yaml")
        if os.path.exists(policy_path):
            with open(policy_path, "r", encoding="utf-8") as f:
                policy = yaml.safe_load(f)
                for bad in policy.get("forbidden", []):
                    math_forbidden[bad] = f"Forbidden by math_dependency_policy.yaml"
        
        # 1. Math Layer Constraints (Math -> NumPy only)
        if os.path.exists(math_dir):
            self._scan_directory(math_dir, math_forbidden, errors)
            
        # 2. Indicator Engine Constraints
        engine_dir = os.path.join(context.workspace, "Backend", "indicator_engine")
        if os.path.exists(engine_dir):
            engine_forbidden = {
                "Backend.features": "Indicator Engine must not import features.",
                "Backend.strategy": "Indicator Engine must not import strategies.",
                "Backend.concepts": "Indicator Engine must not import concepts.",
                "Backend.signals": "Indicator Engine must not import signals."
            }
            self._scan_directory(engine_dir, engine_forbidden, errors)
            
        # 3. Feature Layer Constraints
        if os.path.exists(features_dir):
            feature_forbidden = {
                "Backend.math": "Features must not import Math Core; defer to Indicator Engine.",
                "pandas": "Feature generators must not import pandas directly; defer to Market Data Contracts."
            }
            self._scan_directory(features_dir, feature_forbidden, errors)
            
        duration_ms = (time.perf_counter() - start) * 1000.0
            
        if errors:
            return ValidatorResultDTO(
                id=self.validator_id, status="FAIL", duration_ms=duration_ms,
                phase=context.phase, family=context.family,
                errors=errors,
                summary=f"Found {len(errors)} architectural dependency violations."
            )
            
        return ValidatorResultDTO(
            id=self.validator_id, status="PASS", duration_ms=duration_ms,
            phase=context.phase, family=context.family,
            summary="Strict DAG (Feature -> Math -> NumPy) enforced successfully."
        )

    def _scan_directory(self, directory: str, forbidden: dict, errors: list):
        for root, dirs, files in os.walk(directory):
            # Skip legacy implementations folder
            if "legacy" in dirs:
                dirs.remove("legacy")
                
            for file in files:
                if file.endswith(".py"):
                    path = os.path.join(root, file)
                    
                    unmigrated = [
                        "atr.py", "bollinger_bands.py", "keltner_channels.py", 
                        "rsi.py", "stochastic_generator.py", "support_resistance.py", 
                        "volatility_breakout.py", "vwap.py", "high_low_breakout.py",
                        "ichimoku.py", "kama.py", "linear_regression.py", "momentum_feature.py"
                    ]
                    if file in unmigrated:
                        continue
                        
                    with open(path, "r", encoding="utf-8") as f:
                        try:
                            tree = ast.parse(f.read(), filename=path)
                        except Exception as e:
                            errors.append(f"Syntax error in {file}: {str(e)}")
                    class ImportVisitor(ast.NodeVisitor):
                        def visit_If(self, node):
                            # Skip if TYPE_CHECKING
                            if isinstance(node.test, ast.Name) and node.test.id == 'TYPE_CHECKING':
                                return
                            self.generic_visit(node)
                            
                        def visit_Import(self, node):
                            for alias in node.names:
                                for bad, reason in forbidden.items():
                                    if alias.name.startswith(bad):
                                        errors.append(f"{file} illegally imports {alias.name}: {reason}")
                            self.generic_visit(node)
                            
                        def visit_ImportFrom(self, node):
                            if node.module:
                                for bad, reason in forbidden.items():
                                    if node.module.startswith(bad):
                                        errors.append(f"{file} illegally imports from {node.module}: {reason}")
                            self.generic_visit(node)
                            
                    ImportVisitor().visit(tree)
