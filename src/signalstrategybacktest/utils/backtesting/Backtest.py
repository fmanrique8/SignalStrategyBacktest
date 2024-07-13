"""SignalStrategyBacktest
"""

import pandas as pd


class BacktestProvider:
    """A class to handle backtesting operations."""

    def __init__(self):
        self.data = None

    def load_data(self, df: pd.DataFrame):
        """Load data from a DataFrame."""
        self.data = df
