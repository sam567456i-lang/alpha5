import ast
import os
import pytest

def get_python_files(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                yield os.path.join(root, file)

def check_imports_in_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        try:
            tree = ast.parse(f.read(), filename=filepath)
        except SyntaxError:
            pytest.fail(f"Syntax error in {filepath}")

    violations = []
    # Platform 10 is allowed to import from:
    # Backend.foundation, Backend.core, Backend.platforms.platform9_features, Backend.platforms.platform10_concepts
    allowed_prefixes = (
        "Backend.foundation",
        "Backend.core",
        "Backend.platforms.platform9_features",
        "Backend.platforms.platform10_concepts"
    )

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                module_name = alias.name
                if module_name.startswith("Backend."):
                    if not module_name.startswith(allowed_prefixes):
                        violations.append(module_name)
        elif isinstance(node, ast.ImportFrom):
            if node.module and node.module.startswith("Backend."):
                if not node.module.startswith(allowed_prefixes):
                    violations.append(node.module)

    return violations

def test_platform10_purity():
    """
    Ensures that Platform 10 code ONLY imports from allowed foundation/core/P9 modules.
    Platform 10 must NOT import from Platform 11-14 or Platform 1-8.
    """
    # Assuming tests are run from the project root
    p10_dir = os.path.join("Backend", "platforms", "platform10_concepts")
    
    if not os.path.exists(p10_dir):
        pytest.skip("Platform 10 directory not found. Assuming not yet implemented.")

    all_violations = {}
    for filepath in get_python_files(p10_dir):
        violations = check_imports_in_file(filepath)
        if violations:
            all_violations[filepath] = violations

    if all_violations:
        error_msg = "Platform 10 Purity Violations Found:\n"
        for filepath, violations in all_violations.items():
            error_msg += f"File: {filepath}\n"
            for violation in violations:
                error_msg += f"  - Illegal Import: {violation}\n"
        pytest.fail(error_msg)
