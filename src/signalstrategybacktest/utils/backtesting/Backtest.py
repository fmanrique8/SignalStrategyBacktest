"""SignalStrategyBacktest
"""

import pandas as pd
import yaml


class BacktestProvider:
    """A class to handle backtesting operations."""

    def __init__(self):
        self.data = None
        self.config = None

    def load_data(self, df: pd.DataFrame):
        """Load data from a DataFrame."""
        self.data = df

    def load_base_configuration(self, config: dict):
        """Load the base configuration from a dictionary."""
        self.config = config
        print("Configuration loaded successfully!")
