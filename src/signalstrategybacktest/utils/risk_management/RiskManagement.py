"""SignalStrategyBacktest
"""

import pandas as pd
import numpy as np


class RiskManagement:
    """A class to handle risk management operations."""

    def __init__(
        self, atr_period, support_resistance_window, risk_per_trade, distance_level
    ):
        self.atr_period = atr_period
        self.support_resistance_window = support_resistance_window
        self.risk_per_trade = risk_per_trade
        self.distance_level = distance_level

    def apply(self, df: pd.DataFrame, initial_cash: float) -> pd.DataFrame:
        """Apply ATR and support/resistance levels for risk management."""
        df["ATR"] = self.calculate_atr(df).round(2)
        df["Support"], df["Resistance"] = self.calculate_support_resistance(df)

        df["Stop_Loss"] = df.apply(
            lambda row: (
                round(row["Close"] - row["ATR"], 2)
                if row["signal"] == 1 and not pd.isna(row["ATR"])
                else round(row["Close"] + row["ATR"], 2)
            ),
            axis=1,
        )
        df["Take_Profit"] = df.apply(
            lambda row: (
                round(row["Resistance"], 2)
                if row["signal"] == 1 and not pd.isna(row["Resistance"])
                else round(row["Support"], 2)
            ),
            axis=1,
        )

        # Use .bfill() instead of fillna(method="bfill")
        df.loc[:, "Stop_Loss"] = df["Stop_Loss"].bfill().round(2)
        df.loc[:, "Take_Profit"] = df["Take_Profit"].bfill().round(2)

        df["Position_Size"] = df.apply(
            lambda row: self.calculate_position_size(row, initial_cash), axis=1
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

        # Use .bfill() instead of fillna(method="bfill")
        return atr.bfill().round(2)

    def calculate_support_resistance(self, df: pd.DataFrame) -> (pd.Series, pd.Series):
        """Calculate support and resistance levels."""
        support = df["Low"].rolling(self.support_resistance_window, min_periods=1).min()
        resistance = (
            df["High"].rolling(self.support_resistance_window, min_periods=1).max()
        )

        support = support - (support * self.distance_level)
        resistance = resistance + (resistance * self.distance_level)

        # Use .bfill() instead of fillna(method="bfill")
        return support.bfill().round(2), resistance.bfill().round(2)

    def calculate_position_size(self, row, initial_cash):
        """Calculate position size based on risk per trade."""
        risk_amount = initial_cash * self.risk_per_trade
        if row["signal"] == 1:
            stop_loss_amount = row["Close"] - row["Stop_Loss"]
        else:
            stop_loss_amount = row["Stop_Loss"] - row["Close"]
        position_size = risk_amount / stop_loss_amount if stop_loss_amount != 0 else 0
        return round(position_size, 2)
