import yaml
import os

GOVERNANCE_DIR = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid\Governance\registry"

def create_base_metadata():
    return {
        "supported_markets": ["NSE_Index_Options", "NSE_Futures", "NSE_Cash"],
        "supported_timeframes": ["all"],
        "required_data": [],
        "maturity": "research",
        "implementation_status": "planned"
    }

def generate_analysis_registry():
    families = {
        "Market Context": ["Market regime", "Trend vs Range", "Volatility regime", "Liquidity regime", "Market phase", "Risk On / Risk Off", "Session state", "Time-of-day context", "Cross-market context", "Sector rotation", "Market quality"],
        "Technical": ["SMA", "EMA", "WMA", "HMA", "VWMA", "RSI", "ROC", "MACD", "ADX", "ATR", "Bollinger", "Donchian", "Keltner", "Supertrend", "Ichimoku", "Parabolic SAR"],
        "Trend": ["Primary trend", "Secondary trend", "Micro trend", "Trend continuation", "Trend exhaustion", "Pullback", "Retracement", "Reversal", "Trend strength"],
        "Momentum": ["RSI momentum", "ROC", "MACD", "Histogram", "Momentum acceleration", "Momentum slowdown", "Divergence"],
        "Volatility": ["ATR expansion", "ATR contraction", "Volatility breakout", "Volatility compression", "Standard deviation expansion", "ADR", "Historical volatility", "Volatility regime"],
        "Price Action": ["Swing High", "Swing Low", "HH", "HL", "LH", "LL", "Break & Retest", "False Break", "Compression", "Expansion", "Trendline", "Channel", "Range", "Opening Range", "NR4", "NR7", "Inside Bar", "Outside Bar"],
        "Candlestick": ["Engulfing", "Pin Bar", "Hammer", "Shooting Star", "Morning Star", "Evening Star", "Doji", "Harami", "Marubozu", "Long Wick", "Breakaway Candle", "Momentum Candle", "Exhaustion Candle"],
        "Pattern": ["Double Top", "Double Bottom", "Triangle", "Wedge", "Flag", "Pennant", "Rectangle", "Cup & Handle", "Head & Shoulders", "Inverse Head & Shoulders"],
        "Market Structure": ["BOS", "MSS", "CHOCH", "Internal Structure", "External Structure", "Swing Structure", "Fractal Structure", "Protected High", "Protected Low", "Expansion", "Contraction"],
        "Liquidity": [
            "PDH", "PDL", "PWH", "PWL", "PMH", "PML", "Current Highs/Lows", "Swing Liquidity", "Major Swing", "Minor Swing", "Equal Highs", "Equal Lows", "Triple Tops", "Triple Bottoms", "Session Highs", "Session Lows", "Range Liquidity", "Internal Range Liquidity", "External Range Liquidity", "Premium", "Discount", "Equilibrium", "Liquidity Pools", "Buy Side Liquidity", "Sell Side Liquidity", "Resting Liquidity",
            "Sweep", "Stop Hunt", "Inducement", "Judas Swing", "Turtle Soup", "Liquidity Grab", "Liquidity Raid", "Bull Trap", "Bear Trap", "Fake BOS", "Failed Auction", "Acceptance", "Rejection", "Absorption", "Expansion", "Compression",
            "Order Block", "Breaker", "Mitigation", "Rejection Block", "Propulsion", "Flip Zone", "FVG", "IFVG", "Double FVG", "Stacked FVG", "Volume Imbalance", "Liquidity Void", "BPR", "CE", "Displacement", "Efficient Delivery", "Inefficient Delivery", "HVN", "LVN",
            "Kill Zones", "Sessions", "HTF Bias", "ATR", "ADR", "Trend Context", "Volatility Context", "Market Phase", "Trending", "Ranging", "Accumulation", "Distribution", "Reaccumulation", "Redistribution"
        ],
        "Smart Money": ["Order Blocks", "FVG", "IFVG", "BPR", "Liquidity Void", "Premium", "Discount", "CE", "OTE", "SMT", "Power of Three", "Dealing Range"],
        "Supply & Demand": ["Fresh Zones", "Tested Zones", "Zone Strength", "Zone Age", "Zone Quality", "Zone Imbalance", "Reaction Probability"],
        "Volume": ["VWAP", "Anchored VWAP", "VWAP Bands", "OBV", "CMF", "A/D", "Relative Volume", "Delta", "Buying Pressure", "Selling Pressure", "Volume Divergence", "Volume Climax", "Dry Up", "Effort vs Result"],
        "Volume Profile": ["POC", "VAH", "VAL", "HVN", "LVN", "Naked POC", "Developing POC"],
        "Market Profile": ["Initial Balance", "IB Extension", "Single Prints", "Poor High", "Poor Low", "Excess", "P Shape", "B Shape", "D Shape", "Double Distribution"],
        "Auction Market Theory": ["Failed Auction", "Acceptance", "Rejection", "Balance", "Imbalance", "Rotation"],
        "Wyckoff": ["Accumulation", "Distribution", "Reaccumulation", "Redistribution", "Spring", "Upthrust", "SOS", "SOW", "LPS", "LPSY"],
        "Fibonacci": ["Retracement", "Extension", "Projection", "Expansion", "Golden Pocket", "Clusters", "OTE"],
        "Pivot": ["Classic", "CPR", "Camarilla", "Woodie", "Fibonacci", "DeMark"],
        "Session & Time": ["Asian", "London", "New York", "Daily Open", "Weekly Open", "Monthly Open", "Kill Zones", "Power Hour", "Lunch", "Opening Range"],
        "Multi-Timeframe": ["HTF Bias", "LTF Confirmation", "Alignment", "Conflict", "Confluence"],
        "Options": ["Open Interest", "OI Change", "Long Build-up", "Short Build-up", "Long Unwinding", "Short Covering", "PCR", "Max Pain", "Call Wall", "Put Wall", "Option Chain S/R"],
        "Futures": ["Basis", "Contango", "Backwardation", "OI Structure"],
        "Institutional Flow": ["FII", "DII", "Sector Rotation", "Delivery %", "Block Deals", "Bulk Deals"],
        "Breadth": ["Advance Decline", "Tick", "TRIN", "Participation"],
        "Relative Strength": ["Sector Strength", "Industry Strength", "Relative Weakness"],
        "Correlation": ["Sector", "Index", "Cross Asset"],
        "Economic Events": ["RBI", "CPI", "GDP", "Budget", "Earnings", "PMI"],
        "Fundamental": ["Revenue", "EPS", "Cash Flow", "ROE", "ROCE", "Debt", "Margins", "Valuation"],
        "Sentiment": ["News", "Analyst", "Retail", "Institutional", "Fear & Greed"],
        "Statistical": ["Z Score", "Percentile", "Hurst", "Entropy", "Fractal", "Monte Carlo", "Cointegration", "Kalman"],
        "Machine Learning": ["Regime Classification", "Pattern Classification", "Feature Importance", "Meta Labels", "Anomaly Detection"],
        "Execution": ["Spread", "Slippage", "Fill Quality", "Execution Cost", "Liquidity Availability"],
        "Portfolio": ["Correlation Matrix", "Exposure", "Diversification", "Heat", "Beta", "Alpha"],
        "Risk Observation": ["MAE", "MFE", "Current Drawdown", "Volatility Exposure", "Position Heat"],
        "Performance Observation": ["Historical Strategy Performance", "Historical Market Behavior", "Regime Statistics"],
        "AI Assisted": ["Why price moved", "What analyses agree", "What analyses disagree", "What evidence exists", "What data is missing", "Natural-language explanation"]
    }
    
    registry = {"analyses": []}
    for family, caps in families.items():
        for cap in caps:
            cid = f"ANA_{family.upper().replace(' ', '_').replace('&', 'AND')}_{cap.upper().replace(' ', '_').replace('/', '_')}"
            entry = {
                "capability_id": cid,
                "name": cap,
                "platform": "P06_Analysis",
                "family": family,
                **create_base_metadata()
            }
            if family in ["Order Flow", "Tape Reading"]:
                entry["required_data"].append("Tick")
            if family == "Options":
                entry["required_data"].append("Options Chain")
            if family in ["Macro", "Economic Events"]:
                entry["required_data"].append("Economic Calendar")
            registry["analyses"].append(entry)
            
    with open(os.path.join(GOVERNANCE_DIR, "analysis_registry.yaml"), "w") as f:
        yaml.dump(registry, f, sort_keys=False)

if __name__ == "__main__":
    generate_analysis_registry()
    print("Capability Registries Mass-Generated successfully for all 37 exhaustive families.")
