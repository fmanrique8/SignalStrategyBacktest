"""SignalStrategyBacktest
"""

import pandas as pd


class BollingerBandsStrategy:
    """A class to represent a Bollinger Bands strategy."""

    def __init__(self, window: int, num_std_dev: float):
        self.window = window
        self.num_std_dev = num_std_dev

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply the Bollinger Bands strategy to generate buy/sell signals."""
        df["rolling_mean"] = df["Close"].rolling(window=self.window).mean()
        df["rolling_std"] = df["Close"].rolling(window=self.window).std()
        df["upper_band"] = df["rolling_mean"] + (df["rolling_std"] * self.num_std_dev)
        df["lower_band"] = df["rolling_mean"] - (df["rolling_std"] * self.num_std_dev)
        df["signal"] = 0

        # Buy signal
        df.loc[df["Close"] < df["lower_band"], "signal"] = 1
        # Sell signal
        df.loc[df["Close"] > df["upper_band"], "signal"] = -1

        df["position"] = df["signal"].diff()

        # Round relevant columns to 2 decimal places
        df["rolling_mean"] = df["rolling_mean"].round(2)
        df["rolling_std"] = df["rolling_std"].round(2)
        df["upper_band"] = df["upper_band"].round(2)
        df["lower_band"] = df["lower_band"].round(2)
        df["position"] = df["position"].round(2)

        return df
