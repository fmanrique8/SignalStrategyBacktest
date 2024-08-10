"""SignalStrategyBacktest
"""

import pandas as pd
import numpy as np


class SmaCrossStrategy:
    """A class to represent a simple moving average crossover strategy."""

    def __init__(self, short_window: int, long_window: int):
        self.short_window = short_window
        self.long_window = long_window

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply the SMA crossover strategy to generate buy/sell signals."""
        df["short_mavg"] = (
            df["Close"].rolling(window=self.short_window, min_periods=1).mean()
        )
        df["long_mavg"] = (
            df["Close"].rolling(window=self.long_window, min_periods=1).mean()
        )
        df["signal"] = 0

        # Generate signals when the short moving average crosses the long moving average
        df.loc[df.index[self.short_window :], "signal"] = np.where(
            df["short_mavg"][self.short_window :]
            > df["long_mavg"][self.short_window :],
            1,
            np.where(
                df["short_mavg"][self.short_window :]
                < df["long_mavg"][self.short_window :],
                -1,
                0,
            ),
        )

        # Ensure that signals are generated only when there is a crossover (not continuously)
        df["signal"] = df["signal"].diff().fillna(0)

        # Update positions based on the signal
        df["position"] = (
            df["signal"].cumsum().clip(-1, 1)
        )  # Ensures positions are -1, 0, or 1

        # Round relevant columns to 2 decimal places
        df["short_mavg"] = df["short_mavg"].round(2)
        df["long_mavg"] = df["long_mavg"].round(2)
        df["position"] = df["position"].round(2)

        return df
