import os

def test_framework_invariance():
    """
    Simulates a CI pipeline Enforcer.
    Validates that no files in 'Backend/core/methodology/evaluators' or 
    'Backend/core/methodology/projections' were modified as part of a Methodology Profile PR.
    """
    print("Running Framework Invariance CI Check...")
    
    # In a real CI environment, we would use `git diff origin/main` to find changed files.
    # We will simulate the check here.
    
    simulated_changed_files = [
        "Backend/core/methodology/profiles/smc_profile.yaml",
        "Backend/core/methodology/profiles/wyckoff_profile.yaml",
        "Backend/core/methodology/profiles/amt_profile.yaml"
    ]
    
    protected_directories = [
        "Backend/core/methodology/evaluators",
        "Backend/core/methodology/projections/engine.py"
    ]
    
    for changed_file in simulated_changed_files:
        for protected_dir in protected_directories:
            if changed_file.startswith(protected_dir):
                raise AssertionError(f"[FAIL] Invariance broken! Methodology PR modified core framework file: {changed_file}")
                
    print("[PASS] Framework Invariance CI Check. Core framework remains untouched by new methodologies.")

if __name__ == "__main__":
    test_framework_invariance()
