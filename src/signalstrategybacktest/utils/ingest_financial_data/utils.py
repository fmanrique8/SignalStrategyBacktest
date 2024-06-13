"""SignalStrategyBacktest
"""

import yfinance as yf
import pandas as pd
import logging
from concurrent.futures import ThreadPoolExecutor
import asyncio
from signalstrategybacktest.utils.ingest_financial_data.exceptions import FetchError
from signalstrategybacktest.utils.utils import round_floats, process_datetime

logger = logging.getLogger(__name__)


def select_base_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Select base columns from the DataFrame."""
    return df[["Datetime", "Open", "High", "Low", "Close", "Volume", "Symbol"]]


def fetch_symbol_data(symbol: str, interval: str) -> pd.DataFrame:
    """Fetch data for a single symbol."""
    ticker = yf.Ticker(symbol)
    hist = ticker.history(interval=interval)
    if not hist.empty:
        hist["Symbol"] = symbol
        return hist
    else:
        raise FetchError(symbol)


async def async_fetch_symbol_data(
    symbol: str, interval: str, executor: ThreadPoolExecutor
) -> pd.DataFrame:
    """Fetch data for a single symbol asynchronously using threads."""
    loop = asyncio.get_event_loop()
    try:
        df = await loop.run_in_executor(executor, fetch_symbol_data, symbol, interval)
        return df
    except FetchError as e:
        logger.error(e.message)
        return pd.DataFrame()


def process_data(df: pd.DataFrame, config: dict) -> pd.DataFrame:
    """Process fetched data based on configuration."""
    df = df.reset_index()
    df = process_datetime(df, config)
    df = select_base_columns(df)
    df = round_floats(df)

    return df
