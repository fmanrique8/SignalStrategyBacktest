"""
This is a boilerplate pipeline 'ingest_financial_data'
generated using Kedro 0.19.6
"""

from signalstrategybacktest.utils.ingest_financial_data.DataFetcher import DataFetcher
from signalstrategybacktest.utils.ingest_financial_data.models import BaseConfig
from typing import Any, Dict
import asyncio
import pandas as pd


async def fetch_data_async(
    config: Dict[str, Any], base_config: Dict[str, Any]
) -> pd.DataFrame:
    """Fetch data based on provided configuration asynchronously."""
    config_model = BaseConfig(**config)
    data_fetcher = DataFetcher(config_model, base_config)
    return await data_fetcher.fetch_data()


def fetch_data(config: Dict[str, Any], base_config: Dict[str, Any]) -> pd.DataFrame:
    """Fetch data based on provided configuration."""
    loop = asyncio.get_event_loop()
    if loop.is_running():
        return asyncio.run(fetch_data_async(config, base_config))
    return loop.run_until_complete(fetch_data_async(config, base_config))
