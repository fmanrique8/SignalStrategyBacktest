"""SignalStrategyBacktest
"""


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
