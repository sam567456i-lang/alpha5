import csv
import json
import argparse
from typing import Dict, Any

from Backend.core.platform.adapters.BatchAdapter import BatchAdapter
from Backend.core.platform.measurements.features.volatility import ATR
from Backend.core.platform.measurements.objects.pivot import CenteredPivotEngine
from Backend.core.research.rules.LiquidityLevelRule import LiquidityLevelRule

def calculate_metrics(tp, fp, tn, fn):
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0.0
    return precision, recall, f1, specificity

def run_experiment(descriptor_path: str):
    with open(descriptor_path, 'r') as f:
        desc = json.load(f)
        
    exp_id = desc.get("ExperimentID", "EXP-UNKNOWN")
    csv_path = desc.get("DatasetPath", "Backend/core/research/data/WF-BTCUSDT-2024Q1.csv")
    rule_config = desc.get("RuleConfig", {})
    label_policy = desc.get("LabelPolicy", {})
    
    print(f"--- Starting {exp_id} via Platform 10 Dependency Injection ---")
    
    # 1. Load Data
    bars = []
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            bars.append({
                "timestamp": int(row["timestamp"]),
                "open": float(row["open"]),
                "high": float(row["high"]),
                "low": float(row["low"]),
                "close": float(row["close"])
            })
            
    # 2. Dependency Injection: Orchestrate Platform 10 Execution
    # Instead of manual calculation, we instantiate the requested engines
    atr_engine = ATR({"period": label_policy.get("ATRLength", 21)})
    pivot_engine = CenteredPivotEngine({
        "lookback": rule_config.get("WindowBars", 11) // 2,
        "lookforward": rule_config.get("WindowBars", 11) // 2
    })
    
    batch_atr = BatchAdapter(atr_engine)
    batch_pivot = BatchAdapter(pivot_engine)
    
    print("Running Platform 10 Measurement Pipelines...")
    atr_objects = batch_atr.run_all(bars)
    pivot_objects = batch_pivot.run_all(bars)
    
    atr_values = [obj["value"] if obj else 0.0 for obj in atr_objects]
    
    # 3. Compute Ground Truth for ALL bars using Platform 10 ATR
    REACTION_WINDOW = label_policy.get("ReactionWindow", 20)
    ground_truth = [False] * len(bars)
    reaction_sizes = []
    reaction_delays = []
    
    for i in range(atr_engine.period, len(bars) - REACTION_WINDOW):
        lvl_price = bars[i]["high"]
        is_positive = False
        
        if label_policy.get("Type") == "STATIC":
            threshold = label_policy.get("Threshold", 500.0)
        else:
            mult = label_policy.get("Multiplier", 2.0)
            threshold = atr_values[i] * mult
            
        max_drop = 0
        
        for j in range(i + 1, i + 1 + REACTION_WINDOW):
            if bars[j]["high"] > lvl_price:
                break # Broken
                
            drop = lvl_price - bars[j]["low"]
            if drop > max_drop:
                max_drop = drop
                
            if drop >= threshold and not is_positive:
                is_positive = True
                reaction_delays.append(j - i)
                
        if max_drop > 0:
            reaction_sizes.append(max_drop)
            
        ground_truth[i] = is_positive
        
    avg_delay = sum(reaction_delays) / len(reaction_delays) if reaction_delays else 0
    avg_reaction = sum(reaction_sizes) / len(reaction_sizes) if reaction_sizes else 0
    
    if reaction_sizes:
        sorted_reactions = sorted(reaction_sizes)
        median_reaction = sorted_reactions[len(sorted_reactions)//2]
    else:
        median_reaction = 0
        
    pos_rate = sum(ground_truth) / len(ground_truth)
    
    # 4. Phase 3 Execution (Purely consumes Platform 10)
    rule = LiquidityLevelRule(rule_config)
    platform10_data = {
        "CenteredPivot": pivot_objects,
        "ATR": atr_objects
    }
    
    evidence_list = rule.evaluate(platform10_data)
    
    predictions = [False] * len(bars)
    for ev in evidence_list:
        predictions[ev.bar_index] = True
            
    # 5. Compute Confusion Matrix
    tp = fp = tn = fn = 0
    
    # Regimes
    trending_tp = trending_fp = trending_tn = trending_fn = 0
    ranging_tp = ranging_fp = ranging_tn = ranging_fn = 0
    
    for i in range(rule_config.get("WindowBars", 11), len(bars) - REACTION_WINDOW):
        pred = predictions[i]
        actual = ground_truth[i]
        
        # Regime detection
        is_trending = atr_values[i] > 200 # simple heuristic
            
        if pred and actual:
            tp += 1
            if is_trending: trending_tp += 1
            else: ranging_tp += 1
        elif pred and not actual:
            fp += 1
            if is_trending: trending_fp += 1
            else: ranging_fp += 1
        elif not pred and actual:
            fn += 1
            if is_trending: trending_fn += 1
            else: ranging_fn += 1
        else:
            tn += 1
            if is_trending: trending_tn += 1
            else: ranging_tn += 1
            
    precision, recall, f1, spec = calculate_metrics(tp, fp, tn, fn)
    t_prec, t_rec, t_f1, _ = calculate_metrics(trending_tp, trending_fp, trending_tn, trending_fn)
    r_prec, r_rec, r_f1, _ = calculate_metrics(ranging_tp, ranging_fp, ranging_tn, ranging_fn)
    
    # Save output metadata
    out_data = {
        "TP": tp, "FP": fp, "TN": tn, "FN": fn,
        "Precision": precision, "Recall": recall, "F1": f1,
        "GroundTruth": ground_truth,
        "Predictions": predictions
    }
    
    with open(f"Backend/core/research/{exp_id}_raw.json", "w") as f:
        json.dump(out_data, f)
        
    # Generate Report
    report = f"""# {exp_id}: Detection Quality
*Machine-Generated Execution Summary*

## Immutable Descriptor
```json
{json.dumps(desc, indent=2)}
```

## Global Confusion Matrix
| TP | FP | TN | FN |
|---|---|---|---|
| {tp} | {fp} | {tn} | {fn} |

**Metrics**: Precision: {precision:.2%}, Recall: {recall:.2%}, F1: {f1:.2%}

## Label Statistics
- **Positive Rate**: {pos_rate:.2%}
- **Negative Rate**: {1 - pos_rate:.2%}
- **Average Reaction Size**: ${avg_reaction:.2f}
- **Median Reaction Size**: ${median_reaction:.2f}
- **Detection Delay**: {avg_delay:.1f} bars

## Regime Breakdown
| Regime | TP | FP | FN | Precision | Recall | F1 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Trending** | {trending_tp} | {trending_fp} | {trending_fn} | {t_prec:.2%} | {t_rec:.2%} | {t_f1:.2%} |
| **Ranging** | {ranging_tp} | {ranging_fp} | {ranging_fn} | {r_prec:.2%} | {r_rec:.2%} | {r_f1:.2%} |
"""
    
    report_path = f"Backend/core/research/{exp_id}_Report.md"
    with open(report_path, 'w') as f:
        f.write(report)
        
    print(f"Experiment completed. Report saved to {report_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--descriptor", required=True)
    args = parser.parse_args()
    run_experiment(args.descriptor)
