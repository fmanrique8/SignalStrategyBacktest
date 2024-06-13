"""SignalStrategyBacktest
"""

import pandas as pd
import pytz


def round_floats(df: pd.DataFrame) -> pd.DataFrame:
    """Round all float columns to 2 decimal places."""
    float_cols = df.select_dtypes(include=["float"]).columns
    df[float_cols] = df[float_cols].round(2)
    return df


def process_datetime(df: pd.DataFrame, config: dict) -> pd.DataFrame:
    """Process Datetime column based on the configuration."""
    # Fetch timezone from configuration
    timezone = config["datetime_zone"]

    # Ensure 'Datetime' column is in datetime format
    if not pd.api.types.is_datetime64_any_dtype(df["Datetime"]):
        df["Datetime"] = pd.to_datetime(df["Datetime"])

    # Handle timezone conversion
    if df["Datetime"].dt.tz is None:
        df["Datetime"] = df["Datetime"].dt.tz_localize(pytz.UTC).dt.tz_convert(timezone)
    else:
        df["Datetime"] = df["Datetime"].dt.tz_convert(timezone)

    # Format datetime to yyyy-mm-dd hh:mm
    df["Datetime"] = df["Datetime"].dt.strftime("%Y-%m-%d %H:%M")

    return df
