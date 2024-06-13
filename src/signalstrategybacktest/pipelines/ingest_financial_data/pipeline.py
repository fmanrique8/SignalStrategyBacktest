"""
This is a boilerplate pipeline 'ingest_financial_data'
generated using Kedro 0.19.6
"""

from kedro.pipeline import node, Pipeline

from signalstrategybacktest.pipelines.ingest_financial_data.nodes import (
    fetch_data,
)


def create_pipeline() -> Pipeline:
    """Create Kedro pipeline with different configuration nodes."""
    return Pipeline(
        [
            node(
                func=fetch_data,
                inputs=["params:crypto_configuration", "params:base_configuration"],
                outputs="crypto_source_data",
                name="fetch_crypto_data",
            ),
            node(
                func=fetch_data,
                inputs=["params:forex_configuration", "params:base_configuration"],
                outputs="forex_source_data",
                name="fetch_forex_data",
            ),
            node(
                func=fetch_data,
                inputs=["params:stocks_configuration", "params:base_configuration"],
                outputs="stocks_source_data",
                name="fetch_stocks_data",
            ),
        ]
    )
