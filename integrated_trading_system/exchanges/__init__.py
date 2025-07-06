"""
Exchange Adapters Module
Provides unified interfaces for different cryptocurrency exchanges
"""

from .binance_adapter import (
    BinanceAdapter,
    BinanceOrderSide,
    BinanceOrderType,
    BinanceTicker,
    BinanceOrderBook,
    BinanceOrder,
    BinanceBalance
)

from .backpack_adapter import (
    BackpackAdapter,
    BackpackOrderSide,
    BackpackOrderType,
    BackpackTicker,
    BackpackOrderBook,
    BackpackOrder,
    BackpackBalance
)

__all__ = [
    # Binance
    'BinanceAdapter',
    'BinanceOrderSide',
    'BinanceOrderType',
    'BinanceTicker',
    'BinanceOrderBook',
    'BinanceOrder',
    'BinanceBalance',
    # Backpack
    'BackpackAdapter',
    'BackpackOrderSide',
    'BackpackOrderType',
    'BackpackTicker',
    'BackpackOrderBook',
    'BackpackOrder',
    'BackpackBalance',
]