"""SignalStrategyBacktest
"""

import yfinance as yf
import pandas as pd
from pydantic import BaseModel

from signalstrategybacktest.utils.ingest_financial_data.utils import process_data


class DataFetcher:
    """Class to fetch data from yfinance."""

    def __init__(self, config: BaseModel):
        """Initialize with configuration."""
        self.config = config

    def fetch_data(self) -> pd.DataFrame:
        """Fetch data based on the configuration."""
        data_frames = []
        interval = self.config.time_interval
        symbols = self.config.symbols

        for symbol in symbols:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(interval=interval)
            hist["Symbol"] = symbol
            data_frames.append(hist)

        if data_frames:
            df = pd.concat(data_frames)
            return process_data(df)
        else:
            return pd.DataFrame()  # Return empty DataFrame if no data fetched.
