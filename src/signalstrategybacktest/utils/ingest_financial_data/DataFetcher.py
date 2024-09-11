"""SignalStrategyBacktest
"""

import pandas as pd
import logging
import asyncio
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta

from signalstrategybacktest.utils.ingest_financial_data.exceptions import (
    ProcessError,
)
from signalstrategybacktest.utils.ingest_financial_data.models import BaseConfig
from signalstrategybacktest.utils.ingest_financial_data.utils import (
    process_data,
    async_fetch_symbol_data,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataFetcher:
    """Class to fetch data from yfinance."""

    def __init__(self, config: BaseConfig, base_config: dict):
        """Initialize with configuration."""
        self.config = config
        self.base_config = base_config
        self.executor = ThreadPoolExecutor(max_workers=5)

    def calculate_date_range(self) -> tuple:
        """Calculate start and end dates based on configuration."""
        days_ago = self.config.date_range.get(
            "days_ago", 30
        )  # Default to 30 days if not specified
        end_date = datetime.today()
        start_date = end_date - timedelta(days=days_ago)
        return start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")

    async def fetch_data(self) -> pd.DataFrame:
        """Fetch data based on the configuration."""
        start_date, end_date = self.calculate_date_range()
        tasks = [
            async_fetch_symbol_data(
                symbol, self.config.time_interval, start_date, end_date, self.executor
            )
            for symbol in self.config.symbols
        ]
        data_frames = await asyncio.gather(*tasks)

        data_frames = [df for df in data_frames if not df.empty]

        if data_frames:
            try:
                df = pd.concat(data_frames)
                return process_data(df, self.base_config)
            except Exception as e:
                logger.error(f"Data processing error: {e}")
                raise ProcessError(e)
        else:
            return pd.DataFrame()
