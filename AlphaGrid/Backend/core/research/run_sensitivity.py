import json
import os
import subprocess

SENSITIVITY_DESC = [
    {
        "ExperimentID": "EXP-SENS-1",
        "DatasetPath": "Backend/core/research/data/WF-BTCUSDT-2024Q1.csv",
        "RuleConfig": {"WindowBars": 11},
        "LabelPolicy": {"Type": "STATIC", "Threshold": 500.0, "ReactionWindow": 20},
        "CodeCommit": "HEAD"
    },
    {
        "ExperimentID": "EXP-SENS-2",
        "DatasetPath": "Backend/core/research/data/WF-BTCUSDT-2024Q1.csv",
        "RuleConfig": {"WindowBars": 11},
        "LabelPolicy": {"Type": "ATR_MULTIPLIER", "ATRLength": 21, "Multiplier": 1.0, "ReactionWindow": 20},
        "CodeCommit": "HEAD"
    },
    {
        "ExperimentID": "EXP-SENS-3",
        "DatasetPath": "Backend/core/research/data/WF-BTCUSDT-2024Q1.csv",
        "RuleConfig": {"WindowBars": 11},
        "LabelPolicy": {"Type": "ATR_MULTIPLIER", "ATRLength": 21, "Multiplier": 1.5, "ReactionWindow": 20},
        "CodeCommit": "HEAD"
    },
    {
        "ExperimentID": "EXP-SENS-4",
        "DatasetPath": "Backend/core/research/data/WF-BTCUSDT-2024Q1.csv",
        "RuleConfig": {"WindowBars": 11},
        "LabelPolicy": {"Type": "ATR_MULTIPLIER", "ATRLength": 21, "Multiplier": 2.0, "ReactionWindow": 20},
        "CodeCommit": "HEAD"
    },
    {
        "ExperimentID": "EXP-SENS-5",
        "DatasetPath": "Backend/core/research/data/WF-BTCUSDT-2024Q1.csv",
        "RuleConfig": {"WindowBars": 11},
        "LabelPolicy": {"Type": "ATR_MULTIPLIER", "ATRLength": 21, "Multiplier": 3.0, "ReactionWindow": 20},
        "CodeCommit": "HEAD"
    }
]

def run_sensitivity():
    os.makedirs("Backend/core/research/descriptors", exist_ok=True)
    
    for desc in SENSITIVITY_DESC:
        path = f"Backend/core/research/descriptors/{desc['ExperimentID']}.json"
        with open(path, "w") as f:
            json.dump(desc, f, indent=2)
            
        print(f"Running {desc['ExperimentID']}...")
        subprocess.run(["python", "Backend/core/research/experiment_runner.py", "--descriptor", path], check=True)
        
if __name__ == "__main__":
    run_sensitivity()
