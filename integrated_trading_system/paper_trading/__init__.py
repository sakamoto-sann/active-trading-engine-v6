#!/usr/bin/env python3
"""
Paper Trading Package v1.0.0
Live simulation environment for multi-exchange trading system validation
"""

from .paper_trading_engine import (
    PaperTradingEngine,
    PaperTradingStatus,
    SimulationMode,
    VirtualBalance,
    VirtualOrder,
    VirtualExchange,
    VirtualPortfolio,
    SimulationSettings,
    PaperTradingMetrics,
    AlertConfig,
    AlertManager
)

__all__ = [
    'PaperTradingEngine',
    'PaperTradingStatus',
    'SimulationMode',
    'VirtualBalance',
    'VirtualOrder', 
    'VirtualExchange',
    'VirtualPortfolio',
    'SimulationSettings',
    'PaperTradingMetrics',
    'AlertConfig',
    'AlertManager'
]

__version__ = "1.0.0"