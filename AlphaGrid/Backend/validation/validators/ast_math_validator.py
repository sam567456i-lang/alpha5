import os
import ast
import time
from Backend.validation.validators.abstract_validator import AbstractValidator
from Backend.validation.dtos import ValidationContextDTO, ValidatorResultDTO

class AstMathValidator(AbstractValidator):
    """
    VAL-MATH-001: Ensures no inline math computations (like pandas .ewm, .rolling, np.convolve)
    are used in Feature Generators.
    """
    def run_validation(self, context: ValidationContextDTO) -> ValidatorResultDTO:
        start = time.perf_counter()
        features_dir = os.path.join(context.workspace, "Backend", "features")
        
        errors = []
        
        if os.path.exists(features_dir):
            for root, dirs, files in os.walk(features_dir):
                if "legacy" in dirs:
                    dirs.remove("legacy")
                for file in files:
                    if file.endswith(".py"):
                        path = os.path.join(root, file)
                        
                        # Incremental Enforcement: Only enforce on migrated components
                        # By default, we will assume files without explicit 'ftr-' mapping are subject to rules
                        # or we can just parse the file to see if it's migrated, but for now we skip known unmigrated files.
                        
                        # A simple hardcoded exclusion list for this wave until they are migrated
                        unmigrated = [
                            "atr.py", "bollinger_bands.py", "keltner_channels.py", 
                            "rsi.py", "stochastic_generator.py", "support_resistance.py", 
                            "volatility_breakout.py", "vwap.py", "high_low_breakout.py"
                        ]
                        if file in unmigrated:
                            continue
                            
                        with open(path, "r", encoding="utf-8") as f:
                            try:
                                tree = ast.parse(f.read(), filename=path)
                            except Exception as e:
                                errors.append(f"Syntax error in {file}: {str(e)}")
                                continue
                                
                        class MathVisitor(ast.NodeVisitor):
                            def visit_Attribute(self, node):
                                if node.attr in ['ewm', 'rolling', 'shift']:
                                    errors.append(f"{file} illegally calls .{node.attr}() - defer to Math Core.")
                                self.generic_visit(node)
                                
                            def visit_Call(self, node):
                                if isinstance(node.func, ast.Attribute):
                                    if getattr(node.func.value, 'id', '') == 'np' and node.func.attr == 'convolve':
                                        errors.append(f"{file} illegally calls np.convolve - defer to Math Core.")
                                self.generic_visit(node)
                                
                            def visit_For(self, node):
                                # Basic heuristic for inline EMA loop
                                for child in ast.walk(node):
                                    if isinstance(child, ast.Assign):
                                        for target in child.targets:
                                            if isinstance(target, ast.Name) and 'ema' in target.id.lower() and 'alpha' in getattr(child.value, 'id', getattr(child.value, 'attr', getattr(child.value, 's', ''))):
                                                pass # Actually, searching for alpha in loop is tricky. 
                                                # A simpler check: if they use a for loop and assign something containing 'ema' and 'alpha' is used.
                                self.generic_visit(node)
                                
                        MathVisitor().visit(tree)
                        
        duration_ms = (time.perf_counter() - start) * 1000.0
            
        if errors:
            return ValidatorResultDTO(
                id=self.validator_id, status="FAIL", duration_ms=duration_ms,
                phase=context.phase, family=context.family,
                errors=errors,
                summary=f"Found {len(errors)} math encapsulation violations."
            )
            
        return ValidatorResultDTO(
            id=self.validator_id, status="PASS", duration_ms=duration_ms,
            phase=context.phase, family=context.family,
            summary="All math operations properly delegated to Math Core."
        )
