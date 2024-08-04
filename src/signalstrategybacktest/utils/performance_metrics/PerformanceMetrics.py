"""SignalStrategyBacktest
"""

import pandas as pd

from signalstrategybacktest.utils.performance_metrics.utils import (
    calculate_total_return,
    calculate_average_return_per_trade,
    calculate_final_portfolio_value,
    calculate_total_profit,
    calculate_max_drawdown,
    calculate_sharpe_ratio,
    calculate_sortino_ratio,
    calculate_win_rate,
    calculate_loss_rate,
    calculate_profit_factor,
)


class PerformanceMetrics:
    """A class to calculate and return performance metrics from the order book."""

    def __init__(
        self,
        order_book: pd.DataFrame,
        initial_cash: float,
        risk_free_rate: float = 0.01,
    ):
        self.order_book = order_book
        self.initial_cash = initial_cash
        self.risk_free_rate = risk_free_rate

    def calculate_metrics(self) -> dict:
        """Calculate performance metrics for each symbol."""
        symbols = self.order_book["symbol"].unique()
        performance_metrics = {}

        for symbol in symbols:
            symbol_orders = self.order_book[self.order_book["symbol"] == symbol]
            symbol_cash = self.initial_cash
            total_profit = 0
            total_trades = 0
            win_trades = 0
            loss_trades = 0
            gross_profit = 0
            gross_loss = 0
            daily_returns = []

            order_ids = symbol_orders["order_id"].unique()

            for order_id in order_ids:
                orders = symbol_orders[symbol_orders["order_id"] == order_id]
                if len(orders) == 2:
                    buy_order = orders[orders["order_type"] == "buy"].iloc[0]
                    sell_order = orders[orders["order_type"] == "sell"].iloc[0]

                    if (
                        buy_order["execution_price"] > 0
                        and sell_order["execution_price"] > 0
                    ):
                        buy_price = buy_order["execution_price"]
                        sell_price = sell_order["execution_price"]
                        quantity = buy_order["quantity"]

                        profit = (sell_price - buy_price) * (quantity / buy_price)
                        total_profit += profit
                        total_trades += 1
                        symbol_cash += profit * buy_price
                        daily_returns.append(profit / self.initial_cash)

                        if profit > 0:
                            win_trades += 1
                            gross_profit += profit
                        else:
                            loss_trades += 1
                            gross_loss += abs(profit)

            total_return = calculate_total_return(self.initial_cash, symbol_cash)
            average_return_per_trade = calculate_average_return_per_trade(
                total_profit, total_trades
            )
            final_portfolio_value = calculate_final_portfolio_value(symbol_cash)
            total_profit = calculate_total_profit(total_profit)
            max_drawdown = calculate_max_drawdown(daily_returns)
            sharpe_ratio = calculate_sharpe_ratio(daily_returns, self.risk_free_rate)
            sortino_ratio = calculate_sortino_ratio(daily_returns, self.risk_free_rate)
            win_rate = calculate_win_rate(win_trades, total_trades)
            loss_rate = calculate_loss_rate(loss_trades, total_trades)
            profit_factor = calculate_profit_factor(gross_profit, gross_loss)

            performance_metrics[symbol] = {
                "total_profit": total_profit,
                "total_trades": total_trades,
                "average_return_per_trade": average_return_per_trade,
                "final_portfolio_value": final_portfolio_value,
                "total_return": total_return,
                "max_drawdown": max_drawdown,
                "sharpe_ratio": sharpe_ratio,
                "sortino_ratio": sortino_ratio,
                "win_rate": win_rate,
                "loss_rate": loss_rate,
                "profit_factor": profit_factor,
            }

        return performance_metrics

    def get_metrics(self) -> dict:
        """Return performance metrics as a dictionary."""
        return self.calculate_metrics()
