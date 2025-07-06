"""
Integrated Trading System
Multi-exchange trading system with unified interfaces
"""

from .exchanges import (
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