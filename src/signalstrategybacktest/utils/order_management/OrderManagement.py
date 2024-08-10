"""SignalStrategyBacktest
"""

import pandas as pd
import pytz
from signalstrategybacktest.utils.order_management.utils import (
    calculate_price,
    OrderType,
    create_order,
    generate_order_id,
    get_next_trading_day_close_time,
)


class OrderManagement:
    """A class to manage orders during backtesting."""

    def __init__(
        self,
        slippage=0,
        commission_rate=0,
        close_order_time="15:30",
        timezone="America/New_York",
    ):
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
        self.close_order_time = str(close_order_time)
        self.timezone = timezone

    def apply(self, data: pd.DataFrame):
        """Apply order management to track trades."""
        data["Stop_Loss"] = data["Stop_Loss"].ffill().round(2)
        data["Take_Profit"] = data["Take_Profit"].ffill().round(2)
        data["Datetime"] = pd.to_datetime(data["Datetime"])  # Convert to datetime

        for index, row in data.iterrows():
            signal = row["signal"]
            position = row["position"]
            timestamp = row["Datetime"]
            symbol = row["Symbol"]
            price = calculate_price(row["Close"], self.slippage, self.commission_rate)
            quantity = row["Position_Size"]
            stop_loss = row["Stop_Loss"]
            take_profit = row["Take_Profit"]

            # Ensure position is checked before placing a new order
            closed_position = self.manage_existing_position(
                signal, position, price, timestamp
            )

            # Place a new order only if the position has changed or if no position was previously held
            if signal != 0 and not closed_position:
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
                self._check_time_close(timestamp, price)

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

    def _check_time_close(self, timestamp, price):
        """Check and handle order closure based on time."""
        local_tz = pytz.timezone(self.timezone)
        if timestamp.tzinfo is None:
            timestamp = local_tz.localize(timestamp)

        for order in self.active_orders[:]:
            order_timestamp = pd.to_datetime(order["timestamp"])
            if order_timestamp.tzinfo is None:
                order_timestamp = local_tz.localize(order_timestamp)

            next_close_time = get_next_trading_day_close_time(
                order_timestamp, self.close_order_time, self.timezone
            )
            if timestamp >= next_close_time:
                self._close_order(
                    order, next_close_time.replace(tzinfo=None), price, "time_close"
                )

    def _close_order(self, order, timestamp, price, reason):
        """Close an active order due to stop loss, take profit, or time."""
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

    def manage_existing_position(self, signal, position, price, timestamp):
        """Manages existing positions before placing new orders."""
        if self.active_orders:
            active_order = self.active_orders[0]
            existing_order_type = active_order["order_type"]

            # Close an existing order if the signal is opposite to the current position
            if (signal == 1 and existing_order_type == OrderType.SELL) or (
                signal == -1 and existing_order_type == OrderType.BUY
            ):
                self._close_order(active_order, timestamp, price, "signal_reversal")
                return True  # Indicate that an order was closed

        # If a position is already active and matches the signal, do nothing
        if (position == 1 and signal == 1) or (position == -1 and signal == -1):
            return True  # No need to open a new order

        return False  # No position was closed, and a new order might be needed

    def get_order_book(self):
        """Return the order book DataFrame."""
        return self.order_book
