import ast
import os
import pytest

# Paths to the plugin files
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLATFORM8_DIR = os.path.join(BASE_DIR, "platforms", "platform8_analysis")

LIQUIDITY_STATES_FILE = os.path.join(PLATFORM8_DIR, "liquidity_states.py")
MARKET_STRUCTURE_STATES_FILE = os.path.join(PLATFORM8_DIR, "market_structure_states.py")

def _get_ast(filepath: str) -> ast.Module:
    with open(filepath, "r", encoding="utf-8") as f:
        return ast.parse(f.read(), filename=filepath)

def test_liquidity_plugin_purity():
    """
    Validates that the Liquidity Plugin does not recalculate Geometry (Swings, Extremes).
    It should not contain math for finding highs/lows.
    """
    tree = _get_ast(LIQUIDITY_STATES_FILE)
    
    # Check for forbidden function calls like 'max', 'min' for raw price calculation
    # We will enforce a strict AST walk
    forbidden_calls = {"max", "min"}
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                assert node.func.id not in forbidden_calls, f"Liquidity Plugin must NOT use {node.func.id}(). It must consume upstream Geometry states."

        # It must import Geometry states
        if isinstance(node, ast.ImportFrom):
            if "geometry_states" in node.module:
                imported_names = [alias.name for alias in node.names]
                assert "SwingState" in imported_names or "TimeExtremesState" in imported_names, "Liquidity Plugin must consume SwingState or TimeExtremesState."

def test_market_structure_plugin_purity():
    """
    Validates that the Market Structure Plugin does not recalculate pivots/highs/lows.
    It MUST consume SwingState and LiquidityState.
    """
    tree = _get_ast(MARKET_STRUCTURE_STATES_FILE)
    
    consumes_swing = False
    consumes_liquidity = False
    
    for node in ast.walk(tree):
        # Look for imports of upstream states
        if isinstance(node, ast.ImportFrom):
            if node.module and "geometry_states" in node.module:
                imported_names = [alias.name for alias in node.names]
                if "SwingState" in imported_names:
                    consumes_swing = True
            
            if node.module and "liquidity_states" in node.module:
                imported_names = [alias.name for alias in node.names]
                if "LiquidityState" in imported_names:
                    consumes_liquidity = True
                    
        # Check for forbidden logic
        if isinstance(node, ast.FunctionDef):
            if node.name in ["find_high", "find_low", "calculate_pivot"]:
                pytest.fail(f"Market Structure Plugin MUST NOT compute {node.name}. Those belong upstream in Geometry.")

    assert consumes_swing, "Market Structure Plugin MUST consume SwingState."
    # The requirement didn't strictly say it MUST import LiquidityState, but the user plan said:
    # "Must consume SwingState, LiquidityState". We will enforce it.
    assert consumes_liquidity, "Market Structure Plugin MUST consume LiquidityState."
