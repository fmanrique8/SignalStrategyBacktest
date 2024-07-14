"""
This is a boilerplate pipeline 'backtesting'
generated using Kedro 0.19.6
"""

import pandas as pd
from signalstrategybacktest.utils.backtesting.Backtest import BacktestProvider
from signalstrategybacktest.utils.technical_indicators.SmaCross import SmaCrossStrategy


def backtest_base_strategy_node(
    df: pd.DataFrame, base_config: dict, strategy_config: dict
) -> pd.DataFrame:
    """Kedro node to load data, base configuration, and strategy configuration into the backtesting provider and return
    the same DataFrame."""
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

    return backtest_provider.data
