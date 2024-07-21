"""SignalStrategyBacktest
"""

import pandas as pd

from signalstrategybacktest.utils.order_management.utils import (
    calculate_price,
    OrderType,
    create_order,
    generate_order_id,
)


class OrderManagement:
    """A class to manage orders during backtesting."""

    def __init__(self, slippage=0, commission_rate=0):
        self.order_book = pd.DataFrame(
            columns=[
                "order_id",
                "timestamp",
                "symbol",
                "order_type",
                "quantity",
                "price",
                "execution_price",
                "status",
                "stop_loss",
                "take_profit",
                "trade_reason",
            ]
        )
        self.active_orders = []
        self.slippage = slippage
        self.commission_rate = commission_rate
        self.order_id_counter = 1

    def apply(self, data: pd.DataFrame):
        """Apply order management to track trades."""
        data["Stop_Loss"] = data["Stop_Loss"].ffill().round(2)
        data["Take_Profit"] = data["Take_Profit"].ffill().round(2)

        for index, row in data.iterrows():
            signal = row["signal"]
            position = row["position"]
            timestamp = row["Datetime"]
            symbol = row["Symbol"]
            price = calculate_price(row["Close"], self.slippage, self.commission_rate)
            quantity = row["Position_Size"]
            stop_loss = row["Stop_Loss"]
            take_profit = row["Take_Profit"]

            if signal != 0:
                order_type = OrderType.BUY if signal == 1 else OrderType.SELL
                order_id = generate_order_id(self.order_id_counter)
                self.order_id_counter += 1
                order = create_order(
                    order_id,
                    timestamp,
                    symbol,
                    order_type,
                    quantity,
                    price,
                    price,  # execution price
                    "fulfilled",
                    stop_loss,
                    take_profit,
                    "signal",
                )
                self.order_book = pd.concat([self.order_book, order], ignore_index=True)
                self.active_orders.append(
                    order.iloc[0].to_dict()
                )  # Add the order to active orders as a dictionary

            if self.active_orders:
                self._check_stop_loss_take_profit(timestamp, price)

    def _check_stop_loss_take_profit(self, timestamp, price):
        """Check and handle stop loss and take profit conditions."""
        for order in self.active_orders[:]:
            if (
                order["order_type"] == OrderType.BUY and price <= order["stop_loss"]
            ) or (
                order["order_type"] == OrderType.SELL and price >= order["stop_loss"]
            ):
                self._close_order(order, timestamp, order["stop_loss"], "stop_loss")
            elif (
                order["order_type"] == OrderType.BUY and price >= order["take_profit"]
            ) or (
                order["order_type"] == OrderType.SELL and price <= order["take_profit"]
            ):
                self._close_order(order, timestamp, order["take_profit"], "take_profit")

    def _close_order(self, order, timestamp, price, reason):
        """Close an active order due to stop loss or take profit."""
        order_type = (
            OrderType.SELL if order["order_type"] == OrderType.BUY else OrderType.BUY
        )
        close_order = create_order(
            order["order_id"],
            timestamp,
            order["symbol"],
            order_type,
            order["quantity"],
            price,
            price,
            reason,
            order["stop_loss"],
            order["take_profit"],
            reason,
        )
        self.order_book = pd.concat([self.order_book, close_order], ignore_index=True)
        self.active_orders = [
            o for o in self.active_orders if o["order_id"] != order["order_id"]
        ]  # Remove the order from active orders

    def get_order_book(self):
        """Return the order book DataFrame."""
        return self.order_book
