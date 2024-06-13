"""
This is a boilerplate pipeline 'ingest_financial_data'
generated using Kedro 0.19.6
"""

from signalstrategybacktest.utils.ingest_financial_data.DataFetcher import DataFetcher
from signalstrategybacktest.utils.ingest_financial_data.models import (
    CryptoConfig,
    StockConfig,
    ForexConfig,
    Config,
)

from typing import Dict
import pandas as pd


def fetch_data_node(config_data: dict) -> Dict[str, pd.DataFrame]:
    """Kedro node to fetch data based on configuration dictionary."""
    config = Config(**config_data)

    # Fetch crypto data
    crypto_config = CryptoConfig(**config.crypto_configuration)
    crypto_fetcher = DataFetcher(crypto_config)
    crypto_data = crypto_fetcher.fetch_data()

    # Fetch stocks data
    stocks_config = StockConfig(**config.stocks_configuration)
    stocks_fetcher = DataFetcher(stocks_config)
    stocks_data = stocks_fetcher.fetch_data()

    # Fetch forex data
    forex_config = ForexConfig(**config.forex_configuration)
    forex_fetcher = DataFetcher(forex_config)
    forex_data = forex_fetcher.fetch_data()

    return {
        "crypto_data": crypto_data,
        "stocks_data": stocks_data,
        "forex_data": forex_data,
    }
