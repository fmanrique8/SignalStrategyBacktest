"""
This is a boilerplate pipeline 'ingest_financial_data'
generated using Kedro 0.19.6
"""

from signalstrategybacktest.utils.ingest_financial_data.DataFetcher import DataFetcher
from signalstrategybacktest.utils.ingest_financial_data.models import BaseConfig
from typing import Any, Dict
import pandas as pd


def fetch_data(config: Dict[str, Any], base_config: Dict[str, Any]) -> pd.DataFrame:
    """Fetch data based on provided configuration."""
    config_model = BaseConfig(**config)
    data_fetcher = DataFetcher(config_model, base_config)
    return data_fetcher.fetch_data()
