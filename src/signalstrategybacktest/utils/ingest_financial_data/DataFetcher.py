"""SignalStrategyBacktest
"""

import pandas as pd
import logging
import asyncio
from concurrent.futures import ThreadPoolExecutor

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
        self.executor = ThreadPoolExecutor(
            max_workers=5
        )  # Adjust the number of workers as needed

    async def fetch_data(self) -> pd.DataFrame:
        """Fetch data based on the configuration."""
        tasks = [
            async_fetch_symbol_data(symbol, self.config.time_interval, self.executor)
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
