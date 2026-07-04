import csv

new_capabilities = [
    "Analysis Core", "Trend", "Momentum", "Volatility", "Support/Resistance", "Volume", 
    "Price Action", "Candlestick", "Chart Patterns", "Market Structure", "Smart Money", 
    "Liquidity", "Market Profile", "Order Flow", "Quantitative", "Statistical", 
    "Relative Strength", "Breadth", "Correlation", "Intermarket", "Macro", "Seasonal", 
    "Fundamental", "Sentiment", "Options", "Machine Learning", "AI Analysis", "External Analysis"
]

csv_file = r"Docs/Roadmaps/Master_Capability_Matrix.csv"

with open(csv_file, "a", newline="") as f:
    writer = csv.writer(f)
    for i, cap in enumerate(new_capabilities):
        id_name = cap.replace(" ", "").replace("/", "").upper()
        cap_id = f"AN-{id_name}-{str(i+1).zfill(3)}"
        
        row = [
            cap_id,                        # Capability ID
            f"{cap} Analysis",             # Capability Name
            "Platform 5 (Analysis)",       # Platform
            "Analysis",                    # Program
            "Analysis",                    # Category
            "Planned",                     # Status
            "Indicators",                  # Dependencies
            "Stocks, Crypto, Forex",       # Supported Markets
            "All",                         # Supported Timeframes
            "All",                         # Supported Trading Styles
            cap,                           # Analysis Domains
            "Validation-Profile-AN",       # Validation Profile
            "Benchmark-Profile-AN",        # Benchmark Profile
            "Analysis Explorer",           # Dashboard Module
            "Yes",                         # AI Compatible
            "Planned",                     # Documentation
            "1.0.0",                       # Version
            "ArchitectureTeam",            # Owner
            ""                             # Notes
        ]
        writer.writerow(row)

print("Injected 28 capabilities into Master_Capability_Matrix.csv")
