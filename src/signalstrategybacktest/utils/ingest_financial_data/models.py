"""SignalStrategyBacktest
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any


class CryptoConfig(BaseModel):
    time_interval: str = Field(..., pattern=r"^\d+[mhdw]$")
    symbols: List[str]


class StockConfig(BaseModel):
    time_interval: str = Field(..., pattern=r"^\d+[mhdw]$")
    symbols: List[str]


class ForexConfig(BaseModel):
    time_interval: str = Field(..., pattern=r"^\d+[mhdw]$")
    symbols: List[str]


class Config(BaseModel):
    crypto_configuration: Dict[str, Any]
    stocks_configuration: Dict[str, Any]
    forex_configuration: Dict[str, Any]
