"""SignalStrategyBacktest
"""

import pandas as pd
from signalstrategybacktest.utils.utils import round_floats, process_datetime


def select_base_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Select base columns from the DataFrame."""
    return df[["Datetime", "Open", "High", "Low", "Close", "Volume", "Symbol"]]


def process_data(df: pd.DataFrame, config: dict) -> pd.DataFrame:
    """Process fetched data based on configuration."""
    df = df.reset_index()
    df = process_datetime(df, config)
    df = select_base_columns(df)
    df = round_floats(df)

    return df
