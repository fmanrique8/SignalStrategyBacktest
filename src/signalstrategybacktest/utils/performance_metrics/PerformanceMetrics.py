"""SignalStrategyBacktest
"""

import pandas as pd

from signalstrategybacktest.utils.performance_metrics.utils import (
    calculate_total_return,
    calculate_average_return_per_trade,
    calculate_final_portfolio_value,
    calculate_total_profit,
)


class PerformanceMetrics:
    """A class to calculate and return performance metrics from the order book."""

    def __init__(self, order_book: pd.DataFrame, initial_cash: float):
        self.order_book = order_book
        self.initial_cash = initial_cash

    def calculate_metrics(self) -> dict:
        """Calculate performance metrics for each symbol."""
        symbols = self.order_book["symbol"].unique()
        performance_metrics = {}

        for symbol in symbols:
            symbol_orders = self.order_book[self.order_book["symbol"] == symbol]
            symbol_cash = self.initial_cash
            total_profit = 0
            total_trades = 0

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

            total_return = calculate_total_return(self.initial_cash, symbol_cash)
            average_return_per_trade = calculate_average_return_per_trade(
                total_profit, total_trades
            )
            final_portfolio_value = calculate_final_portfolio_value(symbol_cash)
            total_profit = calculate_total_profit(total_profit)

            performance_metrics[symbol] = {
                "total_profit": total_profit,
                "total_trades": total_trades,
                "average_return_per_trade": average_return_per_trade,
                "final_portfolio_value": final_portfolio_value,
                "total_return": total_return,
            }

        return performance_metrics

    def get_metrics(self) -> dict:
        """Return performance metrics as a dictionary."""
        return self.calculate_metrics()
