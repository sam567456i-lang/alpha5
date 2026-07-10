import json
import os

def build_transition_matrix(baseline_json, target_json):
    with open(baseline_json) as f:
        base = json.load(f)
    with open(target_json) as f:
        tgt = json.load(f)
        
    base_gt = base["GroundTruth"]
    tgt_gt = tgt["GroundTruth"]
    
    matrix = {
        "Pos->Pos": 0,
        "Pos->Neg": 0,
        "Neg->Pos": 0,
        "Neg->Neg": 0
    }
    
    for b, t in zip(base_gt, tgt_gt):
        if b and t: matrix["Pos->Pos"] += 1
        elif b and not t: matrix["Pos->Neg"] += 1
        elif not b and t: matrix["Neg->Pos"] += 1
        else: matrix["Neg->Neg"] += 1
        
    return matrix

def compile_sensitivity_report():
    experiments = ["EXP-SENS-1", "EXP-SENS-2", "EXP-SENS-3", "EXP-SENS-4", "EXP-SENS-5"]
    
    results = {}
    for exp in experiments:
        with open(f"Backend/core/research/{exp}_raw.json") as f:
            results[exp] = json.load(f)
            
    report = "# Label Sensitivity Study (Phase A)\n\n"
    report += "| Experiment | Threshold Policy | Precision | Recall | F1 | Total Positives |\n"
    report += "|---|---|---|---|---|---|\n"
    
    policies = {
        "EXP-SENS-1": "Static $500",
        "EXP-SENS-2": "ATR(21) x 1.0",
        "EXP-SENS-3": "ATR(21) x 1.5",
        "EXP-SENS-4": "ATR(21) x 2.0 (CFG-LABEL-001)",
        "EXP-SENS-5": "ATR(21) x 3.0"
    }
    
    for exp in experiments:
        r = results[exp]
        total_pos = sum(r["GroundTruth"])
        report += f"| {exp} | {policies[exp]} | {r['Precision']:.2%} | {r['Recall']:.2%} | {r['F1']:.2%} | {total_pos} |\n"
        
    report += "\n## Transition Matrices (vs Static $500)\n\n"
    
    for exp in ["EXP-SENS-2", "EXP-SENS-3", "EXP-SENS-4", "EXP-SENS-5"]:
        mat = build_transition_matrix(f"Backend/core/research/EXP-SENS-1_raw.json", f"Backend/core/research/{exp}_raw.json")
        report += f"### {exp} ({policies[exp]})\n"
        report += "| Transition | Count |\n|---|---|\n"
        for k, v in mat.items():
            report += f"| {k} | {v} |\n"
        report += "\n"
        
    with open("Backend/core/research/Label_Sensitivity_Report.md", "w") as f:
        f.write(report)
        
if __name__ == "__main__":
    compile_sensitivity_report()
