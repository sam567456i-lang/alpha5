---
Document ID: KNOW-005
Title: "Breakout Family Migration Manifest & Rollback Plan"
Version: 1.0.0
Governance Version: 1.0.0
Architecture Version: 1.0.0
Phase: 10
Owner: ArchitectureTeam
Category: Knowledge
Maturity: "Level 5: Institutionally Frozen"
Implementation Status: Validated
Current Phase: 10
Future Phase: N/A
Last Validated Phase: 10
Review Date: 2026-07-03
Dependencies: []
Referenced By: []
---

# Breakout Family Migration Manifest & Rollback Plan

## Safe Copies (New Files)

| Relative Path | Status | Action | Rollback | Validation |
|---------------|--------|--------|----------|------------|
| `Backend\concepts\core\breakout.py` | New | ADD | Delete file | Pipeline tests |
| `Backend\concepts\core\extremum.py` | New | ADD | Delete file | Pipeline tests |
| `Backend\dtos\base.py` | New | ADD | Delete file | Import validation |
| `Backend\dtos\concepts.py` | New | ADD | Delete file | Import validation |
| `Backend\dtos\features.py` | New | ADD | Delete file | Import validation |
| `Backend\dtos\methodologies.py` | New | ADD | Delete file | Import validation |
| `Backend\dtos\signals.py` | New | ADD | Delete file | Import validation |
| `Backend\dtos\strategies.py` | New | ADD | Delete file | Import validation |
| `Backend\features\atr.py` | New | ADD | Delete file | Feature tests |
| `Backend\features\bollinger_bands.py` | New | ADD | Delete file | Feature tests |
| `Backend\features\high_low_breakout.py` | New | ADD | Delete file | Feature tests |
| `Backend\features\keltner_channels.py` | New | ADD | Delete file | Feature tests |
| `Backend\features\rsi.py` | New | ADD | Delete file | Feature tests |
| `Backend\features\support_resistance.py` | New | ADD | Delete file | Feature tests |
| `Backend\features\volatility_breakout.py` | New | ADD | Delete file | Feature tests |
| `Backend\features\vwap.py` | New | ADD | Delete file | Feature tests |
| `Backend\features\stochastic_generator.py` | New | ADD (Renamed) | Delete file | Feature tests |
| `Backend\methodologies\breakout.py` | New | ADD | Delete file | Pipeline tests |
| `Backend\methodologies\mean_reversion.py` | New | ADD | Delete file | Pipeline tests |
| `Backend\signals\primitive\generators\breakout_signals.py`| New | ADD | Delete file | Pipeline tests |
| `Backend\signals\primitive\generators\reversion_signals.py`| New | ADD | Delete file | Pipeline tests |
| `Backend\strategy\strategies\bollinger_reversion.py` | New | ADD | Delete file | Strategy tests |
| `Backend\strategy\strategies\breakout_strategies.py` | New | ADD | Delete file | Strategy tests |
| `Backend\strategy\strategies\rsi_reversion.py` | New | ADD | Delete file | Strategy tests |
| `Tests\test_breakout.py` | New | ADD | Delete file | pytest |
| `Tests\test_governance_breakout.py` | New | ADD | Delete file | pytest |

## Modified Files

| Relative Path | Status | Action | Rollback | Validation |
|---------------|--------|--------|----------|------------|
| `Tests\test_features_math.py` | Mod | MERGE | Restore `.bak` | pytest |
| `master_capability_registry.yaml` | Mod | MERGE | Restore `.bak` | Registry validation |
| `Backend\features\__init__.py` | Mod | EDIT | Restore `.bak` | Import validation |
| `Backend\concepts\core\__init__.py` | Mod | EDIT | Restore `.bak` | Import validation |
| `Backend\methodologies\__init__.py` | Mod | EDIT | Restore `.bak` | Import validation |
| `Backend\signals\primitive\generators\__init__.py` | Mod | EDIT | Restore `.bak` | Import validation |
| `Backend\strategy\strategies\__init__.py` | Mod | EDIT | Restore `.bak` | Import validation |
