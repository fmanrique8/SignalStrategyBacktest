"""SignalStrategyBacktest
"""

import pytest
import pandas as pd
from unittest.mock import patch, AsyncMock
from signalstrategybacktest.utils.ingest_financial_data.DataFetcher import DataFetcher
from signalstrategybacktest.utils.ingest_financial_data.models import BaseConfig

# Mock configurations for testing
mock_config = {"time_interval": "15m", "symbols": ["AAPL", "GOOGL", "MSFT"]}

mock_base_config = {"datetime_zone": "America/New_York"}

# Mock DataFrame for testing
mock_dataframe = pd.DataFrame(
    {
        "Datetime": ["2024-05-13 12:30", "2024-05-13 12:45", "2024-05-13 13:00"],
        "Open": [63283.05, 63097.2, 63172.98],
        "High": [63283.05, 63206.2, 63172.98],
        "Low": [63110.09, 63082.5, 62737.81],
        "Close": [63119.98, 63163.38, 62811.48],
        "Volume": [0, 65136640, 86898688],
        "Symbol": ["BTC-USD", "BTC-USD", "BTC-USD"],
    }
)


@pytest.fixture
def data_fetcher():
    """Fixture to provide a DataFetcher instance."""
    config_model = BaseConfig(**mock_config)
    return DataFetcher(config_model, mock_base_config)


@pytest.mark.asyncio
async def test_fetch_data(data_fetcher):
    """Test fetch_data method of DataFetcher class."""
    with patch(
        "signalstrategybacktest.utils.ingest_financial_data.utils.async_fetch_symbol_data",
        new_callable=AsyncMock,
    ) as mock_fetch:
        with patch(
            "signalstrategybacktest.utils.ingest_financial_data.utils.process_data",
            return_value=mock_dataframe,
        ) as mock_process:
            # Mock the async_fetch_symbol_data to return mock data for each call
            mock_fetch.side_effect = [mock_dataframe] * len(mock_config["symbols"])

            result = await data_fetcher.fetch_data()

            # Debugging: print the shapes and data
            print(f"Expected DataFrame shape: {mock_dataframe.shape}")
            print(f"Result DataFrame shape: {result.shape}")
            print("Expected DataFrame:")
            print(mock_dataframe)
            print("Result DataFrame:")
            print(result)

            # Assertions to check if the function behaves as expected
            assert not result.empty, "The result DataFrame should not be empty"
            assert list(result.columns) == list(
                mock_dataframe.columns
            ), "The returned DataFrame should have the same columns as the mock DataFrame"


if __name__ == "__main__":
    pytest.main()
