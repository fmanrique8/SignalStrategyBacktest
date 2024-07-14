"""SignalStrategyBacktest
"""

import pandas as pd


class BacktestProvider:
    """A class to handle backtesting operations."""

    def __init__(self):
        self.data = None
        self.base_config = None
        self.strategy_config = None
        self.strategy = None

    def load_data(self, df: pd.DataFrame):
        """Load data from a DataFrame."""
        self.data = df

    def load_base_configuration(self, config: dict):
        """Load the base configuration from a dictionary."""
        self.base_config = config
        print("Base configuration loaded successfully!")

    def load_strategy_configuration(self, config: dict):
        """Load the strategy configuration from a dictionary."""
        self.strategy_config = config
        print("Strategy configuration loaded successfully!")

    def set_strategy(self, strategy):
        """Set the strategy for backtesting."""
        self.strategy = strategy

    def apply_strategy(self):
        """Apply the strategy to generate buy/sell signals."""
        if self.strategy:
            self.data = self.strategy.apply(self.data)
        else:
            print("No strategy set!")
