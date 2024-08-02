"""
This is a boilerplate pipeline 'backtesting'
generated using Kedro 0.19.6
"""

import pandas as pd
from signalstrategybacktest.utils.backtesting.Backtest import BacktestProvider
from signalstrategybacktest.utils.order_management.OrderManagement import (
    OrderManagement,
)
from signalstrategybacktest.utils.risk_management.RiskManagement import RiskManagement
from signalstrategybacktest.utils.technical_indicators.BollingerBands import (
    BollingerBandsStrategy,
)
from signalstrategybacktest.utils.technical_indicators.SmaCross import SmaCrossStrategy


def bollinger_bands_backtest_strategy_node(
    df: pd.DataFrame, base_config: dict, strategy_config: dict
) -> tuple:
    """Runs backtest using Bollinger Bands strategy on given data and configurations."""
    backtest_provider = BacktestProvider()
    backtest_provider.load_data(df)
    backtest_provider.load_base_configuration(base_config)
    backtest_provider.load_strategy_configuration(strategy_config)

    strategy_params = strategy_config["BollingerBands"]
    strategy = BollingerBandsStrategy(
        window=strategy_params["window"],
        num_std_dev=strategy_params["num_std_dev"],
    )
    backtest_provider.set_strategy(strategy)
    backtest_provider.apply_strategy()

    # Instantiate and set risk management strategy
    risk_management_params = base_config["risk_management"]
    risk_management = RiskManagement(
        atr_period=risk_management_params["atr_period"],
        support_resistance_window=risk_management_params["support_resistance_window"],
        risk_per_trade=risk_management_params["risk_per_trade"],
        distance_level=risk_management_params["distance_level"],
    )
    backtest_provider.set_risk_management(risk_management)
    backtest_provider.apply_risk_management(initial_cash=base_config["initial_cash"])

    # Instantiate and set order management with slippage, commission rate, and close order time from base_config
    order_management = OrderManagement(
        slippage=base_config["slippage"],
        commission_rate=base_config["commission"],
        close_order_time=str(base_config["close_order_time"]),
        timezone=base_config["datetime_zone"],
    )
    backtest_provider.set_order_management(order_management)
    backtest_provider.apply_order_management()

    return backtest_provider.data, backtest_provider.get_order_book()


def sma_cross_backtest_strategy_node(
    df: pd.DataFrame, base_config: dict, strategy_config: dict
) -> tuple:
    """Runs backtest using SMA crossover strategy on given data and configurations."""
    backtest_provider = BacktestProvider()
    backtest_provider.load_data(df)
    backtest_provider.load_base_configuration(base_config)
    backtest_provider.load_strategy_configuration(strategy_config)

    strategy_params = strategy_config["SmaCross"]
    strategy = SmaCrossStrategy(
        short_window=strategy_params["short_window"],
        long_window=strategy_params["long_window"],
    )
    backtest_provider.set_strategy(strategy)
    backtest_provider.apply_strategy()

    # Instantiate and set risk management strategy
    risk_management_params = base_config["risk_management"]
    risk_management = RiskManagement(
        atr_period=risk_management_params["atr_period"],
        support_resistance_window=risk_management_params["support_resistance_window"],
        risk_per_trade=risk_management_params["risk_per_trade"],
        distance_level=risk_management_params["distance_level"],
    )
    backtest_provider.set_risk_management(risk_management)
    backtest_provider.apply_risk_management(initial_cash=base_config["initial_cash"])

    # Instantiate and set order management with slippage and commission rate from base_config
    order_management = OrderManagement(
        slippage=base_config["slippage"], commission_rate=base_config["commission"]
    )
    backtest_provider.set_order_management(order_management)
    backtest_provider.apply_order_management()

    return backtest_provider.data, backtest_provider.get_order_book()
