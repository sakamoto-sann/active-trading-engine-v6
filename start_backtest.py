#!/usr/bin/env python3
"""
🚀 SIMPLE BACKTEST LAUNCHER v1.0.0
Easy-to-use launcher for comprehensive backtesting suite

Usage Examples:
===============================================================================
# Quick test (2 months of data)
python start_backtest.py --quick

# Full 2021-2025 backtest
python start_backtest.py --full

# Custom date range
python start_backtest.py --start 2023-01-01 --end 2024-01-01

# Multiple symbols
python start_backtest.py --symbols BTCUSDT ETHUSDT SOLUSDT --capital 50000 100000

# Conservative testing only
python start_backtest.py --risk conservative --timeframes 1d
===============================================================================
"""

import asyncio
import sys
import os
from datetime import datetime
import argparse

# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

def print_banner():
    """Print startup banner."""
    print("""
🚀 COMPREHENSIVE BACKTESTING SUITE LAUNCHER
===============================================================================
📊 Real Market Data: Binance Historical Data 2021-2025
🏦 Institutional Bot: All 8 Advanced Modules  
💱 Cross-Exchange: Binance + Backpack Arbitrage
⚖️ Delta-Neutral: Grid Trading Strategies
📈 Multi-Cycle: Bull, Bear, Recovery Analysis
===============================================================================
    """)

def get_preset_configs():
    """Get preset configurations."""
    return {
        'quick': {
            'description': 'Quick test with 2 months of recent data',
            'start_date': '2024-10-01',
            'end_date': '2024-12-01',
            'symbols': ['BTCUSDT'],
            'capital': [10000],
            'capital_scenarios': [10000],
            'timeframes': ['1h'],
            'risk_scenarios': ['moderate']
        },
        'demo': {
            'description': 'Demo with 6 months of data',
            'start_date': '2024-06-01',
            'end_date': '2024-12-01',
            'symbols': ['BTCUSDT', 'ETHUSDT'],
            'capital': [10000, 50000],
            'capital_scenarios': [10000, 50000],
            'timeframes': ['1h', '4h'],
            'risk_scenarios': ['conservative', 'moderate']
        },
        'full': {
            'description': 'Complete 2021-2025 analysis',
            'start_date': '2021-01-01',
            'end_date': '2025-01-01',
            'symbols': ['BTCUSDT', 'ETHUSDT', 'BNBUSDT'],
            'capital': [10000, 50000, 100000],
            'capital_scenarios': [10000, 50000, 100000],
            'timeframes': ['1h', '4h', '1d'],
            'risk_scenarios': ['conservative', 'moderate', 'aggressive']
        },
        'bull_2021': {
            'description': '2021 Bull Market Analysis',
            'start_date': '2021-01-01',
            'end_date': '2021-11-30',
            'symbols': ['BTCUSDT', 'ETHUSDT'],
            'capital': [50000, 100000],
            'capital_scenarios': [50000, 100000],
            'timeframes': ['1h', '4h'],
            'risk_scenarios': ['moderate', 'aggressive']
        },
        'bear_2022': {
            'description': '2022 Bear Market Analysis',
            'start_date': '2022-01-01',
            'end_date': '2022-12-31',
            'symbols': ['BTCUSDT', 'ETHUSDT'],
            'capital': [50000, 100000],
            'capital_scenarios': [50000, 100000],
            'timeframes': ['1h', '4h'],
            'risk_scenarios': ['conservative', 'moderate']
        },
        'recovery_2023': {
            'description': '2023 Recovery Analysis',
            'start_date': '2023-01-01',
            'end_date': '2023-12-31',
            'symbols': ['BTCUSDT', 'ETHUSDT'],
            'capital': [50000, 100000],
            'capital_scenarios': [50000, 100000],
            'timeframes': ['1h', '4h'],
            'risk_scenarios': ['moderate']
        }
    }

async def run_backtest_with_config(config):
    """Run backtest with given configuration."""
    try:
        # Import the comprehensive backtest runner
        from run_comprehensive_backtest import ComprehensiveBacktestRunner
        
        # Create runner
        runner = ComprehensiveBacktestRunner(config)
        
        # Execute backtest
        results = await runner.run_full_backtest_suite()
        
        return results
        
    except ImportError as e:
        print(f"❌ Error importing backtest runner: {e}")
        print("Please ensure all required files are present in the directory.")
        return None
    except Exception as e:
        print(f"❌ Error running backtest: {e}")
        import traceback
        traceback.print_exc()
        return None

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Simple launcher for comprehensive backtesting suite",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Preset Examples:
  --quick          Quick 2-month test
  --demo           6-month demo
  --full           Complete 2021-2025 analysis
  --bull-2021      2021 bull market only
  --bear-2022      2022 bear market only
  --recovery-2023  2023 recovery only

Custom Examples:
  --start 2023-01-01 --end 2024-01-01 --symbols BTCUSDT ETHUSDT
  --capital 10000 50000 --timeframes 1h 4h --risk moderate aggressive
        """
    )
    
    # Preset configurations
    preset_group = parser.add_mutually_exclusive_group()
    preset_group.add_argument('--quick', action='store_true', help='Quick test (2 months)')
    preset_group.add_argument('--demo', action='store_true', help='Demo test (6 months)')
    preset_group.add_argument('--full', action='store_true', help='Full analysis (2021-2025)')
    preset_group.add_argument('--bull-2021', action='store_true', help='2021 bull market')
    preset_group.add_argument('--bear-2022', action='store_true', help='2022 bear market')
    preset_group.add_argument('--recovery-2023', action='store_true', help='2023 recovery')
    
    # Custom configuration
    parser.add_argument('--start', type=str, help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end', type=str, help='End date (YYYY-MM-DD)')
    parser.add_argument('--symbols', nargs='+', help='Trading symbols')
    parser.add_argument('--capital', nargs='+', type=float, help='Capital amounts')
    parser.add_argument('--timeframes', nargs='+', help='Timeframes (1h, 4h, 1d)')
    parser.add_argument('--risk', nargs='+', choices=['conservative', 'moderate', 'aggressive'], 
                       help='Risk scenarios')
    parser.add_argument('--output', type=str, help='Output directory')
    
    # Additional options
    parser.add_argument('--list-presets', action='store_true', help='List available presets')
    parser.add_argument('--dry-run', action='store_true', help='Show configuration without running')
    
    return parser.parse_args()

def build_config_from_args(args):
    """Build configuration from command line arguments."""
    presets = get_preset_configs()
    
    # Check for preset configuration
    config = None
    if args.quick:
        config = presets['quick'].copy()
    elif args.demo:
        config = presets['demo'].copy()
    elif args.full:
        config = presets['full'].copy()
    elif args.bull_2021:
        config = presets['bull_2021'].copy()
    elif args.bear_2022:
        config = presets['bear_2022'].copy()
    elif args.recovery_2023:
        config = presets['recovery_2023'].copy()
    else:
        # Default configuration
        config = {
            'start_date': '2024-01-01',
            'end_date': '2024-06-01',
            'symbols': ['BTCUSDT'],
            'capital': [10000],
            'capital_scenarios': [10000],
            'timeframes': ['1h'],
            'risk_scenarios': ['moderate']
        }
    
    # Override with custom arguments
    if args.start:
        config['start_date'] = args.start
    if args.end:
        config['end_date'] = args.end
    if args.symbols:
        config['symbols'] = args.symbols
    if args.capital:
        config['capital'] = args.capital
    if args.timeframes:
        config['timeframes'] = args.timeframes
    if args.risk:
        config['risk_scenarios'] = args.risk
    
    # Ensure capital_scenarios is set (run_comprehensive_backtest expects this field)
    if 'capital' in config:
        config['capital_scenarios'] = config['capital']
    elif 'capital_scenarios' not in config:
        config['capital_scenarios'] = config.get('capital', [10000])
    
    # Convert date strings to datetime objects
    config['start_date'] = datetime.strptime(config['start_date'], '%Y-%m-%d')
    config['end_date'] = datetime.strptime(config['end_date'], '%Y-%m-%d')
    
    # Set output directory
    if args.output:
        config['output_directory'] = args.output
    else:
        # Generate automatic output directory name
        start_str = config['start_date'].strftime('%Y%m%d')
        end_str = config['end_date'].strftime('%Y%m%d')
        symbols_str = '_'.join(config['symbols'][:2])  # First 2 symbols
        config['output_directory'] = f"backtest_{start_str}_{end_str}_{symbols_str}"
    
    return config

def display_config(config):
    """Display configuration summary."""
    print("📊 BACKTEST CONFIGURATION:")
    print("-" * 50)
    print(f"   📅 Period: {config['start_date'].date()} to {config['end_date'].date()}")
    print(f"   💰 Symbols: {', '.join(config['symbols'])}")
    print(f"   💵 Capital: {', '.join(f'${c:,.0f}' for c in config['capital'])}")
    print(f"   🕒 Timeframes: {', '.join(config['timeframes'])}")
    print(f"   ⚠️  Risk Scenarios: {', '.join(config['risk_scenarios'])}")
    print(f"   📁 Output: {config['output_directory']}")
    
    # Calculate estimated duration
    days = (config['end_date'] - config['start_date']).days
    symbols_count = len(config['symbols'])
    timeframes_count = len(config['timeframes'])
    scenarios_count = len(config['capital']) * len(config['risk_scenarios'])
    
    print(f"\n📈 SCOPE ESTIMATION:")
    print(f"   📊 Trading Days: {days}")
    print(f"   🔢 Total Combinations: {scenarios_count}")
    print(f"   📦 Data Points: ~{days * 24 * symbols_count * timeframes_count:,}")
    
    if days <= 60:
        estimated_time = "2-5 minutes"
    elif days <= 365:
        estimated_time = "5-15 minutes"
    elif days <= 730:
        estimated_time = "15-30 minutes"
    else:
        estimated_time = "30-60 minutes"
    
    print(f"   ⏱️  Estimated Time: {estimated_time}")

async def main():
    """Main execution function."""
    print_banner()
    
    try:
        # Parse arguments
        args = parse_arguments()
        
        # Handle list presets
        if args.list_presets:
            print("📋 AVAILABLE PRESETS:")
            print("-" * 50)
            presets = get_preset_configs()
            for name, preset in presets.items():
                print(f"   --{name.replace('_', '-'):<15} {preset['description']}")
                print(f"   {'':15} Period: {preset['start_date']} to {preset['end_date']}")
                print(f"   {'':15} Symbols: {', '.join(preset['symbols'])}")
                print()
            return 0
        
        # Build configuration
        config = build_config_from_args(args)
        
        # Display configuration
        display_config(config)
        
        # Handle dry run
        if args.dry_run:
            print("\n🔍 DRY RUN - Configuration displayed above")
            print("Add --no-dry-run or remove --dry-run to execute backtest")
            return 0
        
        # Confirm execution for long runs
        days = (config['end_date'] - config['start_date']).days
        if days > 365:
            print(f"\n⚠️  WARNING: This is a long-running backtest ({days} days)")
            response = input("Continue? (y/N): ").strip().lower()
            if response != 'y':
                print("Backtest cancelled")
                return 0
        
        # Start backtest
        print(f"\n🚀 STARTING COMPREHENSIVE BACKTEST...")
        print("=" * 60)
        
        results = await run_backtest_with_config(config)
        
        if results:
            print(f"\n✅ BACKTEST COMPLETED SUCCESSFULLY!")
            print(f"📁 Results saved to: {config['output_directory']}")
            print(f"🌐 Open {config['output_directory']}/master_dashboard.html to view results")
            
            # Display key metrics if available
            if 'success_rate' in results:
                print(f"\n📊 QUICK SUMMARY:")
                print(f"   Success Rate: {results['success_rate']:.1%}")
                print(f"   Duration: {results['execution_summary'].get('duration_formatted', 'N/A')}")
        else:
            print(f"\n❌ BACKTEST FAILED")
            print("Check the logs above for error details")
            return 1
        
    except KeyboardInterrupt:
        print(f"\n⏹️  Backtest cancelled by user")
        return 1
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)