"""SignalStrategyBacktest
"""

import pandas as pd


def process_data(df: pd.DataFrame) -> pd.DataFrame:
    """Process fetched data."""
    df.reset_index(inplace=True)
    df = df[["Datetime", "Open", "High", "Low", "Close", "Volume", "Symbol"]]
    return df
