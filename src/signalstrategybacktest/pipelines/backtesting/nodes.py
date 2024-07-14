"""
This is a boilerplate pipeline 'backtesting'
generated using Kedro 0.19.6
"""

import pandas as pd
from signalstrategybacktest.utils.backtesting.Backtest import BacktestProvider
from signalstrategybacktest.utils.technical_indicators.BollingerBands import (
    BollingerBandsStrategy,
)
from signalstrategybacktest.utils.technical_indicators.SmaCross import SmaCrossStrategy


def sma_cross_backtest_strategy_node(
    df: pd.DataFrame, base_config: dict, strategy_config: dict
) -> pd.DataFrame:
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
    backtest_provider.apply_risk_management()

    return backtest_provider.data


def bollinger_bands_backtest_strategy_node(
    df: pd.DataFrame, base_config: dict, strategy_config: dict
) -> pd.DataFrame:
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
    backtest_provider.apply_risk_management()

    return backtest_provider.data
