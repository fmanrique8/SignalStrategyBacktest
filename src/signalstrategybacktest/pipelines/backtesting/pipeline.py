"""
This is a boilerplate pipeline 'backtesting'
generated using Kedro 0.19.6
"""

from kedro.pipeline import Pipeline, node

from signalstrategybacktest.pipelines.backtesting.nodes import (
    sma_cross_backtest_strategy_node,
    bollinger_bands_backtest_strategy_node,
)


def create_pipeline() -> Pipeline:
    """Create Kedro pipeline with different configuration nodes."""
    return Pipeline(
        [
            node(
                func=sma_cross_backtest_strategy_node,
                inputs=[
                    "stocks_source_data",
                    "params:base_configuration",
                    "params:strategies_configuration",
                ],
                outputs=[
                    "stocks_sma_cross_backtesting_data",
                    "stocks_sma_cross_order_book",
                ],
                name="backtest_stocks_sma_cross_strategy_node",
            ),
            node(
                func=bollinger_bands_backtest_strategy_node,
                inputs=[
                    "stocks_source_data",
                    "params:base_configuration",
                    "params:strategies_configuration",
                ],
                outputs=[
                    "stocks_bollinger_bands_backtesting_data",
                    "stocks_bollinger_bands_order_book",
                ],
                name="backtest_stocks_bollinger_bands_strategy_node",
            ),
        ]
    )
