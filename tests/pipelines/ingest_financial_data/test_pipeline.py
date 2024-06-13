"""
This is a boilerplate test file for pipeline 'ingest_financial_data'
generated using Kedro 0.19.6.
Please add your pipeline tests here.

Kedro recommends using `pytest` framework, more info about it can be found
in the official documentation:
https://docs.pytest.org/en/latest/getting-started.html
"""

import pytest
from pandas import DataFrame
from signalstrategybacktest.pipelines.ingest_financial_data.pipeline import (
    create_pipeline,
)

# Mock data to simulate fetch_data outputs with expected columns
mock_crypto_data = DataFrame(
    {
        "Datetime": [],
        "Open": [],
        "High": [],
        "Low": [],
        "Close": [],
        "Volume": [],
        "Symbol": [],
    }
)
mock_forex_data = DataFrame(
    {
        "Datetime": [],
        "Open": [],
        "High": [],
        "Low": [],
        "Close": [],
        "Volume": [],
        "Symbol": [],
    }
)
mock_stocks_data = DataFrame(
    {
        "Datetime": [],
        "Open": [],
        "High": [],
        "Low": [],
        "Close": [],
        "Volume": [],
        "Symbol": [],
    }
)


@pytest.fixture
def mock_fetch_data(mocker):
    """Mock the fetch_data function."""
    return mocker.patch(
        "signalstrategybacktest.pipelines.ingest_financial_data.nodes.fetch_data"
    )


def test_create_pipeline(mock_fetch_data):
    """Test the pipeline creation and its node outputs."""
    # Set the return values for the fetch_data mock
    mock_fetch_data.side_effect = [mock_crypto_data, mock_forex_data, mock_stocks_data]

    # Create the pipeline
    pipeline = create_pipeline()

    # Assert the pipeline has the correct number of nodes
    assert len(pipeline.nodes) == 3

    # Define the inputs for the nodes
    crypto_inputs = {
        "params:crypto_configuration": {
            "time_interval": "15m",
            "symbols": ["BTC-USD", "ETH-USD", "BNB-USD", "ADA-USD", "DOGE-USD"],
        },
        "params:base_configuration": {"datetime_zone": "America/New_York"},
    }
    forex_inputs = {
        "params:forex_configuration": {
            "time_interval": "15m",
            "symbols": ["EURUSD=X", "JPY=X", "GBPUSD=X", "AUDUSD=X", "USDCAD=X"],
        },
        "params:base_configuration": {"datetime_zone": "America/New_York"},
    }
    stocks_inputs = {
        "params:stocks_configuration": {
            "time_interval": "15m",
            "symbols": ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA"],
        },
        "params:base_configuration": {"datetime_zone": "America/New_York"},
    }

    # Execute each node manually and check the output
    crypto_result = pipeline.nodes[0].run(crypto_inputs)
    forex_result = pipeline.nodes[1].run(forex_inputs)
    stocks_result = pipeline.nodes[2].run(stocks_inputs)

    # Print the results for initial inspection
    print("Crypto Result:", crypto_result)
    print("Forex Result:", forex_result)
    print("Stocks Result:", stocks_result)

    # Assert the results are not empty and have the expected columns
    assert not crypto_result["crypto_source_data"].empty
    assert set(crypto_result["crypto_source_data"].columns) == {
        "Datetime",
        "Open",
        "High",
        "Low",
        "Close",
        "Volume",
        "Symbol",
    }

    assert not forex_result["forex_source_data"].empty
    assert set(forex_result["forex_source_data"].columns) == {
        "Datetime",
        "Open",
        "High",
        "Low",
        "Close",
        "Volume",
        "Symbol",
    }

    assert not stocks_result["stocks_source_data"].empty
    assert set(stocks_result["stocks_source_data"].columns) == {
        "Datetime",
        "Open",
        "High",
        "Low",
        "Close",
        "Volume",
        "Symbol",
    }


if __name__ == "__main__":
    pytest.main([__file__])
