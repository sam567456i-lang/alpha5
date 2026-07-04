import yaml

REGISTRY_PATH = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid\Governance\registry\master_capability_registry.yaml"

with open(REGISTRY_PATH, "r") as f:
    registry = yaml.safe_load(f) or {"capabilities": []}
caps = registry.setdefault("capabilities", [])

def register_placeholder(cid, name, category, family, platform="P05_Analysis"):
    exists = any(c.get("capability_id") == cid for c in caps)
    if not exists:
        caps.append({
            "capability_id": cid,
            "name": name,
            "platform": platform,
            "category": category,
            "family": family,
            "status": "planned"
        })
        print(f"Registered {cid}")

# 1. Technical
tech_fams = ["Trend", "Momentum", "Volatility", "Volume", "Price Action", "Candlestick", 
             "Chart Patterns", "Breakout", "Mean Reversion", "Support Resistance", 
             "Market Structure", "Multi Timeframe"]
for fam in tech_fams:
    cid = f"ANALYSIS_TECH_{fam.replace(' ', '').upper()}"
    register_placeholder(cid, f"{fam} Analysis", "Technical", fam)

# 2. Institutional / Smart Money
smc_fams = ["Smart Money Concepts", "Liquidity", "Order Flow", "Volume Profile", 
            "Market Profile", "Auction Market Theory", "Footprint Analysis", 
            "DOM Analysis", "Delta Analysis", "Iceberg Detection", "Absorption", "Large Order Tracking"]
for fam in smc_fams:
    cid = f"ANALYSIS_INST_{fam.replace(' ', '').upper()}"
    register_placeholder(cid, f"{fam} Analysis", "Institutional", fam)

# 3. Quantitative
quant_fams = ["Statistical", "Quantitative", "Factor Models", "Cointegration", "PCA", 
              "Hidden Markov Models", "Bayesian Models", "Kalman Filter", "Monte Carlo", "Regime Switching"]
for fam in quant_fams:
    cid = f"ANALYSIS_QUANT_{fam.replace(' ', '').upper()}"
    register_placeholder(cid, f"{fam} Analysis", "Quantitative", fam)

# 4. Market Analysis
mkt_fams = ["Relative Strength", "Breadth", "Correlation", "Intermarket", "Sector Rotation", 
            "Currency Strength", "Volatility Regime"]
for fam in mkt_fams:
    cid = f"ANALYSIS_MKT_{fam.replace(' ', '').upper()}"
    register_placeholder(cid, f"{fam} Analysis", "Market Analysis", fam)

# 5. Fundamental
fund_fams = ["Fundamental", "Earnings", "Financial Statements", "Valuation", "Management", "Industry", "Economic"]
for fam in fund_fams:
    cid = f"ANALYSIS_FUND_{fam.replace(' ', '').upper()}"
    register_placeholder(cid, f"{fam} Analysis", "Fundamental", fam)

# 6. Macro
macro_fams = ["Central Bank", "Inflation", "Interest Rates", "Alternative Data"]
for fam in macro_fams:
    cid = f"ANALYSIS_MACRO_{fam.replace(' ', '').upper()}"
    register_placeholder(cid, f"{fam} Analysis", "Macro", fam)

# 7. Sentiment
sent_fams = ["Sentiment", "Behavioral", "News", "Social Media", "On chain", 
             "Options", "Futures Positioning", "COT Analysis"]
for fam in sent_fams:
    cid = f"ANALYSIS_SENT_{fam.replace(' ', '').upper()}"
    register_placeholder(cid, f"{fam} Analysis", "Sentiment", fam)

# 8. AI
ai_fams = ["Machine Learning", "AI Analysis", "Ensemble Analysis", "Meta Analysis", "Explainability Analysis"]
for fam in ai_fams:
    cid = f"ANALYSIS_AI_{fam.replace(' ', '').upper()}"
    register_placeholder(cid, f"{fam} Analysis", "AI", fam)

# 9. External
ext_fams = ["External Repository", "Knowledge Base", "Research Paper"]
for fam in ext_fams:
    cid = f"ANALYSIS_EXT_{fam.replace(' ', '').upper()}"
    register_placeholder(cid, f"{fam} Analysis", "External", fam)

# 10. Strategies (P10_Strategies)
strats = ["Trend Following", "Breakout", "Mean Reversion", "Momentum", "Price Action", 
          "Smart Money", "Volume", "Order Flow", "Statistical", "Machine Learning", 
          "Macro", "Seasonal", "Options"]
for fam in strats:
    cid = f"STRATEGY_{fam.replace(' ', '').upper()}"
    register_placeholder(cid, f"{fam} Strategy", "Strategy", fam, platform="P10_Strategies")

with open(REGISTRY_PATH, "w") as f:
    yaml.dump(registry, f, sort_keys=False)

print("Expanded taxonomy placeholders registered.")
