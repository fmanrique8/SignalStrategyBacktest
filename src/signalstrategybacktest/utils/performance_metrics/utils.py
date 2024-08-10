"""SignalStrategyBacktest
"""

import numpy as np


def calculate_total_return(initial_cash: float, final_cash: float) -> float:
    """Calculate total return."""
    return round((final_cash - initial_cash) / initial_cash * 100, 2)


def calculate_average_return_per_trade(total_profit: float, total_trades: int) -> float:
    """Calculate average return per trade."""
    return round(total_profit / total_trades if total_trades > 0 else 0, 2)


def calculate_final_portfolio_value(cash: float) -> float:
    """Calculate final portfolio value."""
    return round(cash, 2)


def calculate_total_profit(total_profit: float) -> float:
    """Calculate total profit."""
    return round(total_profit, 2)


def calculate_max_drawdown(daily_returns: list) -> float:
    """Calculate maximum drawdown."""
    cumulative_returns = np.cumsum(daily_returns)
    peak = np.maximum.accumulate(cumulative_returns)
    drawdown = (cumulative_returns - peak) / peak
    max_drawdown = np.min(drawdown)
    return round(max_drawdown * 100, 2)


def calculate_sharpe_ratio(daily_returns: list, risk_free_rate: float) -> float:
    """Calculate Sharpe Ratio."""
    excess_returns = np.array(daily_returns) - risk_free_rate / 252
    sharpe_ratio = np.mean(excess_returns) / np.std(excess_returns) * np.sqrt(252)
    return round(sharpe_ratio, 2)


def calculate_sortino_ratio(daily_returns: list, risk_free_rate: float) -> float:
    """Calculate Sortino Ratio."""
    excess_returns = np.array(daily_returns) - risk_free_rate / 252
    downside_returns = excess_returns[excess_returns < 0]
    sortino_ratio = np.mean(excess_returns) / np.std(downside_returns) * np.sqrt(252)
    return round(sortino_ratio, 2)


def calculate_win_rate(win_trades: int, total_trades: int) -> float:
    """Calculate win rate."""
    return round(win_trades / total_trades * 100 if total_trades > 0 else 0, 2)


def calculate_loss_rate(loss_trades: int, total_trades: int) -> float:
    """Calculate loss rate."""
    return round(loss_trades / total_trades * 100 if total_trades > 0 else 0, 2)


def calculate_profit_factor(gross_profit: float, gross_loss: float) -> float:
    """Calculate profit factor."""
    return round(gross_profit / gross_loss if gross_loss > 0 else np.inf, 2)
