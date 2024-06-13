"""SignalStrategyBacktest
"""

import yfinance as yf
import pandas as pd
import logging

from signalstrategybacktest.utils.ingest_financial_data.exceptions import (
    FetchError,
    ProcessError,
)
from signalstrategybacktest.utils.ingest_financial_data.models import BaseConfig
from signalstrategybacktest.utils.ingest_financial_data.utils import process_data

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataFetcher:
    """Class to fetch data from yfinance."""

    def __init__(self, config: BaseConfig, base_config: dict):
        """Initialize with configuration."""
        self.config = config
        self.base_config = base_config

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
                else:
                    raise FetchError(symbol)
            except (ValueError, IndexError, KeyError) as e:
                logger.error(f"Failed to fetch data for {symbol}: {e}")
                continue
            except Exception as e:
                logger.error(f"Unexpected error for {symbol}: {e}")
                continue

        if data_frames:
            try:
                df = pd.concat(data_frames)
                return process_data(df, self.base_config)
            except Exception as e:
                logger.error(f"Data processing error: {e}")
                raise ProcessError(e)
        else:
            return pd.DataFrame()  # Return empty DataFrame if no data fetched.
