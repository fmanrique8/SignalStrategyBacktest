"""
This is a boilerplate pipeline 'backtesting'
generated using Kedro 0.19.6
"""

from kedro.pipeline import Pipeline, node

from signalstrategybacktest.pipelines.backtesting.nodes import (
    backtest_base_strategy_node,
)


def create_pipeline() -> Pipeline:
    """Create Kedro pipeline with different configuration nodes."""
    return Pipeline(
        [
            node(
                func=backtest_base_strategy_node,
                inputs=["stocks_source_data", "params:base_configuration"],
                outputs="stocks_intermediate_data",
                name="backtest_stocks_base_strategy_node",
            ),
        ]
    )
