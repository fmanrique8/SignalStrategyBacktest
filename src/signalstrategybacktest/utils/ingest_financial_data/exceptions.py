"""SignalStrategyBacktest
"""


class DataFetcherError(Exception):
    """Base class for exceptions in DataFetcher."""


class FetchError(DataFetcherError):
    """Exception raised for errors in the fetch process."""

    def __init__(self, symbol):
        self.message = f"Failed to fetch data for symbol: {symbol}"
        super().__init__(self.message)


class ProcessError(DataFetcherError):
    """Exception raised for errors in the data processing."""

    def __init__(self, error):
        self.message = f"Data processing error: {error}"
        super().__init__(self.message)
