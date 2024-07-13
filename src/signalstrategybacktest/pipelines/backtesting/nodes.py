"""
This is a boilerplate pipeline 'backtesting'
generated using Kedro 0.19.6
"""

import pandas as pd
from signalstrategybacktest.utils.backtesting.Backtest import BacktestProvider


def backtest_base_strategy_node(df: pd.DataFrame, config: dict) -> pd.DataFrame:
    """Kedro node to load data and base configuration into the backtesting provider and return the same DataFrame."""
    backtest_provider = BacktestProvider()
    backtest_provider.load_data(df)
    backtest_provider.load_base_configuration(config)
    return backtest_provider.data
