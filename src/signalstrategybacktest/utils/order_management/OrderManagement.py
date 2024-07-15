"""SignalStrategyBacktest
"""

import pandas as pd
import uuid


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
        self.current_position = 0
        self.slippage = slippage
        self.commission_rate = commission_rate

    def apply(self, data):
        """Apply order management to track trades."""
        for index, row in data.iterrows():
            signal = row["signal"]
            position = row["position"]
            timestamp = row["Datetime"]
            symbol = row["Symbol"]
            price = round(
                row["Close"] * (1 + self.slippage) * (1 + self.commission_rate), 2
            )
            quantity = row["Position_Size"]
            stop_loss = round(row["Stop_Loss"], 2)
            take_profit = round(row["Take_Profit"], 2)
            execution_price = (
                price  # Assuming execution price is the same as price for simplicity
            )

            if signal != 0:
                order_id = str(uuid.uuid4())
                order_type = "buy" if signal == 1 else "sell"
                status = "fulfilled"
                trade_reason = "signal"

                # Record the order
                self.order_book = pd.concat(
                    [
                        self.order_book,
                        pd.DataFrame(
                            [
                                {
                                    "order_id": order_id,
                                    "timestamp": timestamp,
                                    "symbol": symbol,
                                    "order_type": order_type,
                                    "quantity": quantity,
                                    "price": price,
                                    "execution_price": execution_price,
                                    "status": status,
                                    "stop_loss": stop_loss,
                                    "take_profit": take_profit,
                                    "trade_reason": trade_reason,
                                }
                            ]
                        ),
                    ],
                    ignore_index=True,
                )

                # Update current position
                self.current_position = position

            # Check for stop loss and take profit conditions
            if self.current_position != 0:
                if (self.current_position == 1 and price <= stop_loss) or (
                    self.current_position == -1 and price >= stop_loss
                ):
                    # Trigger stop loss
                    order_id = str(uuid.uuid4())
                    order_type = "sell" if self.current_position == 1 else "buy"
                    status = "stop_loss"
                    trade_reason = "stop_loss"

                    self.order_book = pd.concat(
                        [
                            self.order_book,
                            pd.DataFrame(
                                [
                                    {
                                        "order_id": order_id,
                                        "timestamp": timestamp,
                                        "symbol": symbol,
                                        "order_type": order_type,
                                        "quantity": quantity,
                                        "price": stop_loss,
                                        "execution_price": stop_loss,
                                        "status": status,
                                        "stop_loss": stop_loss,
                                        "take_profit": take_profit,
                                        "trade_reason": trade_reason,
                                    }
                                ]
                            ),
                        ],
                        ignore_index=True,
                    )

                    self.current_position = 0

                elif (self.current_position == 1 and price >= take_profit) or (
                    self.current_position == -1 and price <= take_profit
                ):
                    # Trigger take profit
                    order_id = str(uuid.uuid4())
                    order_type = "sell" if self.current_position == 1 else "buy"
                    status = "take_profit"
                    trade_reason = "take_profit"

                    self.order_book = pd.concat(
                        [
                            self.order_book,
                            pd.DataFrame(
                                [
                                    {
                                        "order_id": order_id,
                                        "timestamp": timestamp,
                                        "symbol": symbol,
                                        "order_type": order_type,
                                        "quantity": quantity,
                                        "price": take_profit,
                                        "execution_price": take_profit,
                                        "status": status,
                                        "stop_loss": stop_loss,
                                        "take_profit": take_profit,
                                        "trade_reason": trade_reason,
                                    }
                                ]
                            ),
                        ],
                        ignore_index=True,
                    )

                    self.current_position = 0

    def get_order_book(self):
        """Return the order book DataFrame."""
        return self.order_book
