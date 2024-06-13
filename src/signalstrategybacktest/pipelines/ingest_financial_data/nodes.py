"""
This is a boilerplate pipeline 'ingest_financial_data'
generated using Kedro 0.19.6
"""

from signalstrategybacktest.utils.ingest_financial_data.DataFetcher import DataFetcher
from signalstrategybacktest.utils.ingest_financial_data.models import (
    CryptoConfig,
    ForexConfig,
    StockConfig,
)

from typing import Dict, Any
import pandas as pd


def fetch_crypto_data(config: Dict[str, Any]) -> pd.DataFrame:
    """Node to fetch crypto data."""
    crypto_config = CryptoConfig(**config)
    crypto_fetcher = DataFetcher(crypto_config)
    return crypto_fetcher.fetch_data()


def fetch_forex_data(config: Dict[str, Any]) -> pd.DataFrame:
    """Node to fetch forex data."""
    forex_config = ForexConfig(**config)
    forex_fetcher = DataFetcher(forex_config)
    return forex_fetcher.fetch_data()


def fetch_stocks_data(config: Dict[str, Any]) -> pd.DataFrame:
    """Node to fetch stocks data."""
    stocks_config = StockConfig(**config)
    stocks_fetcher = DataFetcher(stocks_config)
    return stocks_fetcher.fetch_data()
