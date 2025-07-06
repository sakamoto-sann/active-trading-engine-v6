"""
Integrated Multi-Exchange System
Unified trading system supporting multiple cryptocurrency exchanges
"""

from .integrated_trading_system import (
    BinanceAdapter,
    BackpackAdapter,
    BinanceOrderSide,
    BinanceOrderType,
    BackpackOrderSide,
    BackpackOrderType
)

__version__ = "1.0.0"

__all__ = [
    'BinanceAdapter',
    'BackpackAdapter',
    'BinanceOrderSide',
    'BinanceOrderType',
    'BackpackOrderSide',
    'BackpackOrderType',
]