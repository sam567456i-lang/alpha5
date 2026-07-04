import csv
import os

base_dir = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid"
matrix_path = os.path.join(base_dir, "Docs", "Roadmaps", "Master_Capability_Matrix.csv")

headers = [
    "Capability ID", "Capability Name", "Platform", "Program", "Category", 
    "Status", "Dependencies", "Supported Markets", "Supported Timeframes", 
    "Supported Trading Styles", "Analysis Domains", "Validation Profile", 
    "Benchmark Profile", "Dashboard Module", "AI Compatible", "Documentation", 
    "Version", "Owner", "Notes"
]

capabilities = [
    # Governance & Data
    {"id": "CAP-001", "name": "Configuration System", "platform": "Platform 1 (Governance)", "prog": "Foundation", "cat": "System", "stat": "Frozen", "deps": "None"},
    {"id": "CAP-002", "name": "Market Data Contracts", "platform": "Platform 2 (Data)", "prog": "Data", "cat": "Contract", "stat": "Planned", "deps": "None"},
    
    # State & Math Core
    {"id": "CAP-010", "name": "Numba Core", "platform": "Platform 7 (Math Core)", "prog": "Engine", "cat": "Math", "stat": "Frozen", "deps": "None"},
    {"id": "CAP-011", "name": "Rolling State Buffer", "platform": "Platform 8 (State Engine)", "prog": "Engine", "cat": "State", "stat": "Planned", "deps": "CAP-010"},
    
    # Indicator Engine: Waves 1-4 (Already Implemented/Frozen theoretically, but we are at Wave 5)
    {"id": "CAP-020", "name": "SMA", "platform": "Platform 9 (Indicator Engine)", "prog": "Analytics", "cat": "Indicator", "stat": "Implemented", "deps": "CAP-011"},
    {"id": "CAP-021", "name": "EMA", "platform": "Platform 9 (Indicator Engine)", "prog": "Analytics", "cat": "Indicator", "stat": "Implemented", "deps": "CAP-011"},
    
    # Wave 5: Extremum
    {"id": "CAP-030", "name": "Donchian Channels", "platform": "Platform 9 (Indicator Engine)", "prog": "Analytics", "cat": "Indicator", "stat": "Planned", "deps": "CAP-011"},
    {"id": "CAP-031", "name": "Support/Resistance", "platform": "Platform 9 (Indicator Engine)", "prog": "Analytics", "cat": "Indicator", "stat": "Planned", "deps": "CAP-011"},
    {"id": "CAP-032", "name": "High/Low", "platform": "Platform 9 (Indicator Engine)", "prog": "Analytics", "cat": "Indicator", "stat": "Planned", "deps": "CAP-011"},
    
    # Wave 6A: RMA & RSI
    {"id": "CAP-033", "name": "RMA", "platform": "Platform 9 (Indicator Engine)", "prog": "Analytics", "cat": "Indicator", "stat": "Planned", "deps": "CAP-011"},
    {"id": "CAP-034", "name": "RSI", "platform": "Platform 9 (Indicator Engine)", "prog": "Analytics", "cat": "Indicator", "stat": "Planned", "deps": "CAP-033"},
    
    # Wave 6B: Momentum
    {"id": "CAP-035", "name": "ROC", "platform": "Platform 9 (Indicator Engine)", "prog": "Analytics", "cat": "Indicator", "stat": "Planned", "deps": "CAP-011"},
    {"id": "CAP-036", "name": "Momentum Engine", "platform": "Platform 9 (Indicator Engine)", "prog": "Analytics", "cat": "Engine", "stat": "Planned", "deps": "CAP-035"},
    
    # Wave 7: Volume
    {"id": "CAP-037", "name": "VWAP", "platform": "Platform 9 (Indicator Engine)", "prog": "Analytics", "cat": "Indicator", "stat": "Planned", "deps": "CAP-011"},
    {"id": "CAP-038", "name": "OBV", "platform": "Platform 9 (Indicator Engine)", "prog": "Analytics", "cat": "Indicator", "stat": "Planned", "deps": "CAP-011"},
    {"id": "CAP-039", "name": "Volume SMA", "platform": "Platform 9 (Indicator Engine)", "prog": "Analytics", "cat": "Indicator", "stat": "Planned", "deps": "CAP-011"},
    {"id": "CAP-040", "name": "Accumulation/Distribution", "platform": "Platform 9 (Indicator Engine)", "prog": "Analytics", "cat": "Indicator", "stat": "Planned", "deps": "CAP-011"},
    
    # Future Intelligence Layers
    {"id": "CAP-050", "name": "Feature Engine", "platform": "Platform 10 (Feature)", "prog": "Intelligence", "cat": "Engine", "stat": "Planned", "deps": "CAP-020"},
    {"id": "CAP-060", "name": "Concept Fusion", "platform": "Platform 11 (Concept)", "prog": "Intelligence", "cat": "Concept", "stat": "Planned", "deps": "CAP-050"},
    {"id": "CAP-070", "name": "Decision Intelligence Fusion", "platform": "Platform 13 (Decision)", "prog": "Intelligence", "cat": "Engine", "stat": "Planned", "deps": "CAP-060"},
    {"id": "CAP-080", "name": "Executive Dashboard", "platform": "Platform 20 (Dashboard)", "prog": "Product", "cat": "UI Module", "stat": "Planned", "deps": "CAP-070"},
]

def default_row(cap):
    return [
        cap.get("id", ""),
        cap.get("name", ""),
        cap.get("platform", ""),
        cap.get("prog", ""),
        cap.get("cat", ""),
        cap.get("stat", ""),
        cap.get("deps", ""),
        "Equities, Crypto, Futures", # Markets
        "All", # Timeframes
        "All", # Styles
        "Technical", # Domains
        "Math, Warmup, Equivalence", # Validation Profile
        "Pandas-TA 100%", # Benchmark
        "Analysis Explorer", # Dashboard Module
        "Yes", # AI Compatible
        "Missing", # Documentation
        "1.0.0", # Version
        "Indicator Team", # Owner
        "" # Notes
    ]

with open(matrix_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    for cap in capabilities:
        writer.writerow(default_row(cap))

print(f"Generated {len(capabilities)} capabilities into {matrix_path}")
