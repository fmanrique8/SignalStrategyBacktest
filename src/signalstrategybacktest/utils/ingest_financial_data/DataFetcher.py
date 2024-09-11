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
    """Class to fetch data from yfinance with dynamic pagination support."""

    def __init__(self, config: BaseConfig, base_config: dict):
        """Initialize with configuration."""
        self.config = config
        self.base_config = base_config
        self.executor = ThreadPoolExecutor(max_workers=5)
        self.chunk_size_days = 59  # Set 59 to safely comply with the 60-day limit

    def calculate_date_ranges(self) -> list:
        """Calculate the date ranges split into chunks of 59 days."""
        days_ago = self.config.date_range.get("days_ago", 30)
        end_date = datetime.today()
        start_date = end_date - timedelta(days=days_ago)

        date_ranges = []
        while start_date < end_date:
            chunk_end = min(start_date + timedelta(days=self.chunk_size_days), end_date)
            date_ranges.append(
                (start_date.strftime("%Y-%m-%d"), chunk_end.strftime("%Y-%m-%d"))
            )
            start_date = chunk_end + timedelta(seconds=1)  # Avoid overlap

        return date_ranges

    async def fetch_data_chunk(
        self, symbol: str, start_date: str, end_date: str
    ) -> pd.DataFrame:
        """Fetch data for a symbol in a specific date range chunk."""
        return await async_fetch_symbol_data(
            symbol, self.config.time_interval, start_date, end_date, self.executor
        )

    async def fetch_data(self) -> pd.DataFrame:
        """Fetch data across multiple paginated date ranges."""
        date_ranges = self.calculate_date_ranges()

        tasks = []
        for symbol in self.config.symbols:
            for start_date, end_date in date_ranges:
                tasks.append(self.fetch_data_chunk(symbol, start_date, end_date))

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
