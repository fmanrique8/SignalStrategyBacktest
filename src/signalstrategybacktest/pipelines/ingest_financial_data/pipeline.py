"""
This is a boilerplate pipeline 'ingest_financial_data'
generated using Kedro 0.19.6
"""

from kedro.pipeline import node, Pipeline

from signalstrategybacktest.pipelines.ingest_financial_data.nodes import fetch_data_node


def create_pipeline() -> Pipeline:
    """Create Kedro pipeline with different configuration nodes."""
    return Pipeline(
        [
            node(
                func=fetch_data_node,
                inputs="params:config",
                outputs=dict(
                    crypto_data="crypto_source_data",
                    stocks_data="stock_source_data",
                    forex_data="forex_source_data",
                ),
                name="fetch_data_node",
            )
        ]
    )
