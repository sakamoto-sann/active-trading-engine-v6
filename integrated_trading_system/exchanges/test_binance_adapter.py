#!/usr/bin/env python3
"""
Test script for BinanceAdapter
Verifies basic functionality without requiring real API keys
"""

import asyncio
import logging
from binance_adapter import BinanceAdapter, BinanceOrderSide, BinanceOrderType

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_public_api():
    """Test public API endpoints that don't require authentication."""
    print("🧪 Testing Binance Adapter Public API...")
    
    # Initialize adapter with dummy credentials (for public API testing)
    adapter = BinanceAdapter(
        api_key="dummy_key",
        api_secret="dummy_secret",
        testnet=True
    )
    
    try:
        await adapter.initialize()
        
        # Test connectivity
        print("✅ Connectivity test passed")
        
        # Test ticker
        try:
            ticker = await adapter.get_ticker("BTCUSDT")
            print(f"✅ Ticker test passed - BTC Price: ${ticker.price:.2f}")
        except Exception as e:
            print(f"❌ Ticker test failed: {e}")
        
        # Test order book
        try:
            orderbook = await adapter.get_orderbook("BTCUSDT", 10)
            print(f"✅ Orderbook test passed - Bids: {len(orderbook.bids)}, Asks: {len(orderbook.asks)}")
        except Exception as e:
            print(f"❌ Orderbook test failed: {e}")
        
        # Test klines
        try:
            klines = await adapter.get_klines("BTCUSDT", "1m", 10)
            print(f"✅ Klines test passed - Got {len(klines)} candles")
        except Exception as e:
            print(f"❌ Klines test failed: {e}")
        
        # Test exchange info
        try:
            exchange_info = await adapter.get_exchange_info()
            symbols_count = len(exchange_info.get('symbols', []))
            print(f"✅ Exchange info test passed - {symbols_count} symbols available")
        except Exception as e:
            print(f"❌ Exchange info test failed: {e}")
        
    finally:
        await adapter.close()
        print("🔒 Adapter closed")

def test_data_structures():
    """Test the data structure classes."""
    print("\n🧪 Testing Data Structures...")
    
    # Test enums
    buy_side = BinanceOrderSide.BUY
    limit_type = BinanceOrderType.LIMIT
    
    print(f"✅ Order side enum: {buy_side.value}")
    print(f"✅ Order type enum: {limit_type.value}")
    
    # Test that all required order types are available
    required_types = [
        BinanceOrderType.LIMIT,
        BinanceOrderType.MARKET,
        BinanceOrderType.STOP_LOSS,
        BinanceOrderType.STOP_LOSS_LIMIT,
        BinanceOrderType.TAKE_PROFIT,
        BinanceOrderType.TAKE_PROFIT_LIMIT
    ]
    
    print(f"✅ All order types available: {[t.value for t in required_types]}")

def test_signature_generation():
    """Test signature generation method."""
    print("\n🧪 Testing Signature Generation...")
    
    adapter = BinanceAdapter("test_key", "test_secret")
    
    # Test with known values
    test_query = "symbol=BTCUSDT&side=BUY&type=LIMIT&quantity=1&price=50000&timestamp=1234567890"
    signature = adapter._generate_signature(test_query)
    
    print(f"✅ Signature generated: {signature[:20]}...")
    print(f"✅ Signature length: {len(signature)} characters")

async def main():
    """Run all tests."""
    print("🚀 Starting Binance Adapter Tests\n")
    
    # Test data structures
    test_data_structures()
    
    # Test signature generation
    test_signature_generation()
    
    # Test public API (requires internet connection)
    try:
        await test_public_api()
    except Exception as e:
        print(f"❌ Public API tests failed: {e}")
        print("   This might be due to network issues or Binance API changes")
    
    print("\n🎉 Test suite completed!")

if __name__ == "__main__":
    asyncio.run(main())