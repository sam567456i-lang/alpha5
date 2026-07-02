"""Metrics Calculator."""

import numpy as np
from typing import List, Dict, Any
from Backend.research.evaluation.report import ProfitabilityMetrics, RiskMetrics, RobustnessMetrics, StatisticalMetrics

class MetricsCalculator:
    """Pure functions for computing quantitative metrics from trade lists and equity curves."""

    @staticmethod
    def calculate_profitability(trades: List[Dict[str, Any]], initial_capital: float = 100000.0) -> ProfitabilityMetrics:
        if not trades:
            return ProfitabilityMetrics(0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
            
        pnls = [t.get("pnl", 0.0) for t in trades]
        gross_profit = sum(p for p in pnls if p > 0)
        gross_loss = abs(sum(p for p in pnls if p < 0))
        
        wins = [p for p in pnls if p > 0]
        losses = [p for p in pnls if p <= 0]
        
        total_trades = len(trades)
        win_rate = len(wins) / total_trades if total_trades > 0 else 0.0
        
        profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else (999.0 if gross_profit > 0 else 0.0)
        
        avg_win = np.mean(wins) if wins else 0.0
        avg_loss = abs(np.mean(losses)) if losses else 0.0
        
        payoff_ratio = (avg_win / avg_loss) if avg_loss > 0 else (999.0 if avg_win > 0 else 0.0)
        expectancy = (win_rate * avg_win) - ((1 - win_rate) * avg_loss)
        
        total_return = sum(pnls) / initial_capital
        
        # Approximate annualized return (assuming 1 year for now, this needs actual timestamps in prod)
        annualized_return = total_return
        
        return ProfitabilityMetrics(
            total_return=float(total_return),
            annualized_return=float(annualized_return),
            win_rate=float(win_rate),
            profit_factor=float(profit_factor),
            expectancy=float(expectancy),
            payoff_ratio=float(payoff_ratio)
        )

    @staticmethod
    def calculate_risk(equity_curve: List[float], risk_free_rate: float = 0.0) -> RiskMetrics:
        if not equity_curve or len(equity_curve) < 2:
            return RiskMetrics(0.0, 0.0, 0.0, 0.0, 0.0)
            
        curve = np.array(equity_curve)
        
        # Drawdown
        roll_max = np.maximum.accumulate(curve)
        drawdowns = (curve - roll_max) / roll_max
        max_dd = abs(float(np.min(drawdowns)))
        
        # Returns
        returns = np.diff(curve) / curve[:-1]
        
        # Volatility & Sharpe (Annualized assuming daily data)
        mean_ret = np.mean(returns)
        std_ret = np.std(returns)
        
        if std_ret == 0:
            sharpe = 0.0
            sortino = 0.0
        else:
            sharpe = float((mean_ret - (risk_free_rate/252)) / std_ret * np.sqrt(252))
            
            downside_returns = returns[returns < 0]
            downside_std = np.std(downside_returns) if len(downside_returns) > 0 else 0.0
            
            if downside_std == 0:
                sortino = 999.0 if mean_ret > 0 else 0.0
            else:
                sortino = float((mean_ret - (risk_free_rate/252)) / downside_std * np.sqrt(252))
                
        # Calmar
        annualized_ret = (curve[-1] / curve[0]) - 1.0  # Simple approx
        calmar = float(annualized_ret / max_dd) if max_dd > 0 else (999.0 if annualized_ret > 0 else 0.0)
        
        # VaR (Historical 95%)
        var_95 = float(np.percentile(returns, 5))
        
        return RiskMetrics(
            max_drawdown=max_dd,
            sharpe_ratio=sharpe,
            sortino_ratio=sortino,
            calmar_ratio=calmar,
            var_95=var_95
        )

    @staticmethod
    def calculate_statistics(trades: List[Dict[str, Any]]) -> StatisticalMetrics:
        total_trades = len(trades)
        if total_trades < 2:
            return StatisticalMetrics(total_trades, 0.0, 0.0)
            
        pnls = [t.get("pnl", 0.0) for t in trades]
        mean_pnl = np.mean(pnls)
        std_pnl = np.std(pnls)
        
        if std_pnl == 0:
            t_stat = 0.0
        else:
            t_stat = float(mean_pnl / (std_pnl / np.sqrt(total_trades)))
            
        # Mock Monte Carlo Survival (would be calculated via actual MC paths in prod)
        mc_survival = 1.0 if t_stat > 1.96 else 0.5
        
        return StatisticalMetrics(
            total_trades=total_trades,
            t_stat=t_stat,
            monte_carlo_survival=mc_survival
        )
        
    @staticmethod
    def calculate_robustness(is_sharpe: float, oos_sharpe: float) -> RobustnessMetrics:
        """Walk-Forward Efficiency (Out-Of-Sample Sharpe / In-Sample Sharpe)"""
        wfe = (oos_sharpe / is_sharpe) if is_sharpe > 0 else 0.0
        
        return RobustnessMetrics(
            walk_forward_efficiency=float(wfe),
            parameter_stability=1.0 # Placeholder
        )
