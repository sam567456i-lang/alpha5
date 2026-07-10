import json
import os
import subprocess

EXP3_DESC = {
    "ExperimentID": "EXP-000003",
    "DatasetPath": "Backend/core/research/data/WF-BTCUSDT-2024Q1.csv",
    "RuleConfig": {"WindowBars": 21},
    "LabelPolicy": {"Type": "STATIC", "Threshold": 500.0, "ReactionWindow": 20},
    "CodeCommit": "HEAD"
}

def run_exp3():
    os.makedirs("Backend/core/research/descriptors", exist_ok=True)
    path = "Backend/core/research/descriptors/EXP-000003.json"
    with open(path, "w") as f:
        json.dump(EXP3_DESC, f, indent=2)
        
    print("Running EXP-000003...")
    subprocess.run(["python", "Backend/core/research/experiment_runner.py", "--descriptor", path], check=True)
    subprocess.run(["cp", "Backend/core/research/EXP-000003_Report.md", "C:\\Users\\praka\\.gemini\\antigravity\\brain\\3e0f9d7c-700c-4ecd-979b-4fddca4f9249\\EXP-000003_Report.md"])

if __name__ == "__main__":
    run_exp3()
