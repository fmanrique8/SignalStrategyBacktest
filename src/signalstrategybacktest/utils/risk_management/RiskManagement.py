"""SignalStrategyBacktest
"""

import pandas as pd
import numpy as np


class RiskManagement:
    """A class to handle risk management operations."""

    def __init__(self, atr_period, support_resistance_window):
        self.atr_period = atr_period
        self.support_resistance_window = support_resistance_window

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply ATR and support/resistance levels for risk management."""
        df["ATR"] = self.calculate_atr(df).round(2)
        df["Support"], df["Resistance"] = self.calculate_support_resistance(df)

        df["Stop_Loss"] = df.apply(
            lambda row: (
                round(row["Close"] - row["ATR"], 2)
                if row["signal"] == 1
                else round(row["Close"] + row["ATR"], 2)
            ),
            axis=1,
        )
        df["Take_Profit"] = df.apply(
            lambda row: (
                round(row["Resistance"], 2)
                if row["signal"] == 1
                else round(row["Support"], 2)
            ),
            axis=1,
        )

        return df

    def calculate_atr(self, df: pd.DataFrame) -> pd.Series:
        """Calculate the Average True Range (ATR)."""
        high_low = df["High"] - df["Low"]
        high_close = np.abs(df["High"] - df["Close"].shift())
        low_close = np.abs(df["Low"] - df["Close"].shift())
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = ranges.max(axis=1)
        atr = true_range.rolling(self.atr_period).mean()
        return atr

    def calculate_support_resistance(self, df: pd.DataFrame) -> (pd.Series, pd.Series):
        """Calculate support and resistance levels."""
        support = df["Low"].rolling(self.support_resistance_window, min_periods=1).min()
        resistance = (
            df["High"].rolling(self.support_resistance_window, min_periods=1).max()
        )
        return support, resistance
