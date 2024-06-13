"""SignalStrategyBacktest
"""

from pydantic import BaseModel, Field
from typing import List


class BaseConfig(BaseModel):
    """Base configuration model."""

    time_interval: str = Field(..., pattern=r"^\d+[mhdw]$")
    symbols: List[str]
