"""SignalStrategyBacktest
"""

import pandas as pd
from datetime import datetime, timedelta
import pytz


class OrderType:
    """Represents types of orders in a trading system."""

    BUY = "buy"
    SELL = "sell"


def create_order(
    order_id: int,
    timestamp: pd.Timestamp,
    symbol: str,
    order_type: OrderType,
    quantity: int,
    price: float,
    execution_price: float,
    status: str,
    stop_loss: float,
    take_profit: float,
    trade_reason: str,
) -> pd.DataFrame:
    """Create a new order DataFrame row."""
    order = pd.DataFrame(
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
    )
    return order


def calculate_price(
    close_price: float, slippage: float, commission_rate: float
) -> float:
    """Calculate the adjusted price with slippage and commission."""
    return round(close_price * (1 + slippage) * (1 + commission_rate), 2)


def generate_order_id(counter: int) -> str:
    """Generate a human-readable and standardized order ID."""
    return f"ORD-{counter:06d}"


def get_next_trading_day_close_time(
    timestamp: datetime, close_time: str, timezone: str
) -> datetime:
    """Get the next trading day's close time."""
    local_tz = pytz.timezone(timezone)
    if timestamp.tzinfo is None:
        timestamp = local_tz.localize(timestamp)
    current_day = timestamp.date()
    next_day = current_day + timedelta(days=1)
    next_close_time = datetime.combine(
        next_day, datetime.strptime(close_time, "%H:%M").time()
    )
    next_close_time = local_tz.localize(next_close_time)
    return next_close_time
