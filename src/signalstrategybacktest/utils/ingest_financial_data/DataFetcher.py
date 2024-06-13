"""SignalStrategyBacktest
"""

import yfinance as yf
import pandas as pd
import logging

from signalstrategybacktest.utils.ingest_financial_data.models import BaseConfig
from signalstrategybacktest.utils.ingest_financial_data.utils import process_data

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataFetcher:
    """Class to fetch data from yfinance."""

    def __init__(self, config: BaseConfig):
        """Initialize with configuration."""
        self.config = config

    def fetch_data(self) -> pd.DataFrame:
        """Fetch data based on the configuration."""
        data_frames = []
        interval = self.config.time_interval
        symbols = self.config.symbols

        for symbol in symbols:
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(interval=interval)
                if not hist.empty:
                    hist["Symbol"] = symbol
                    data_frames.append(hist)
            except Exception:
                pass  # Handle errors as needed

        if data_frames:
            df = pd.concat(data_frames)
            return process_data(df)  # Use the imported process_data function
        else:
            return pd.DataFrame()  # Return empty DataFrame if no data fetched.
