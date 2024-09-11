"""SignalStrategyBacktest
"""

from pydantic import BaseModel, Field
from typing import List, Dict


class BaseConfig(BaseModel):
    """Base configuration model."""

    time_interval: str = Field(..., pattern=r"^\d+[mhdw]$")
    symbols: List[str]
    date_range: Dict[str, int]
