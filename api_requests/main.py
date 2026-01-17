"""
Complete Orchestrator: Fetch data, calculate indicators, score stocks
"""

import time
import sys
import os
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api_requests.nse_nifty500_list import get_nifty_500_stocks
from api_requests.yfinance_stock_data import get_stock_data
from api_requests.nselib_oi_fetcher import get_oi_data

# Import indicator calculators
from indicators.yfinance_data.volume import calculate_volume_ma
from indicators.yfinance_data.macd import calculate_macd
from indicators.yfinance_data.rsi import calculate_rsi
from indicators.yfinance_data.ema_50 import calculate_ema_50
from indicators.yfinance_data.ema_20 import calculate_ema_20
from indicators.yfinance_data.adx import calculate_adx

# Import scorer
from indicators.scorer import score_stock


def calculate_all_indicators(df):
    """
    Calculate all technical indicators for a stock
    
    Args:
        df: DataFrame with OHLCV data
    
    Returns:
        DataFrame with all indicators added
    """
    # Make a copy to avoid modifying original
    df = df.copy()
    
    # Flatten multi-level columns if they exist
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    
    # Calculate all indicators
    df = calculate_volume_ma(df)
    df = calculate_macd(df)
    df = calculate_rsi(df)
    df = calculate_ema_50(df)
    df = calculate_ema_20(df)
    df = calculate_adx(df)
    
    return df


def process_stock(symbol, yf_symbol):
    """
    Process a single stock: fetch data, calculate indicators, score
    
    Args:
        symbol: Stock symbol (e.g., 'RELIANCE')
        yf_symbol: Yahoo Finance symbol (e.g., 'RELIANCE.NS')
    
    Returns:
        Dict with symbol, scores, and latest data
    """
    try:
        # Fetch data
        df = get_stock_data(yf_symbol, days=60)
        
        # Get OI data (with timeout protection)
        oi_pattern = get_oi_data(symbol)
        
        # Calculate indicators
        df = calculate_all_indicators(df)
        
        # Calculate scores
        scores = score_stock(df, oi_pattern)
        
        # Get latest price info
        latest = df.iloc[-1]
        
        result = {
            'symbol': symbol,
            'price': float(latest['Close']),
            'volume': int(latest['Volume']),
            'volume_ratio': float(latest.get('volume_ratio', 0)),
            'rsi': float(latest.get('rsi', 0)),
            'macd': float(latest.get('macd', 0)),
            'ema_20': float(latest.get('ema_20', 0)),
            'ema_50': float(latest.get('ema_50', 0)),
            'adx': float(latest.get('adx', 0)),
            'oi_pattern': oi_pattern,
            'scores': scores,
            'total_score': float(scores['total'])
        }
        
        # Print detailed output
        print(f"✅ Score: {scores['total']:.1f}/80")
        print(f"   OI Pattern: {oi_pattern or 'None'}")
        print(f"   Price: ₹{latest['Close']:.2f}")
        print(f"   RSI: {latest.get('rsi', 0):.2f}")
        print(f"   Volume Ratio: {latest.get('volume_ratio', 0):.2f}x")
        print(f"   ADX: {latest.get('adx', 0):.2f}")
        
        return result
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return None


def fetch_and_score_all_stocks(limit=None):
    """
    Main orchestrator: Fetch, calculate, score all stocks
    
    Args:
        limit: Limit number of stocks (for testing)
    
    Returns:
        List of stock results sorted by score
    """
    
    print("="*60)
    print("STEP 1: Fetching NIFTY 500 stock list")
    print("="*60)
    
    stocks = get_nifty_500_stocks()
    stock_list = [s for s in stocks if s['symbol'] != 'NIFTY 500']
    
    if limit:
        stock_list = stock_list[:limit]
        print(f"⚠️  Testing mode: Processing {limit} stocks\n")
    
    print(f"✅ Got {len(stock_list)} stocks to process\n")
    
    print("="*60)
    print("STEP 2: Fetching data, calculating indicators, and scoring")
    print("="*60)
    
    results = []
    successful = 0
    failed = 0
    
    for i, stock in enumerate(stock_list, 1):
        symbol = stock['symbol']
        yf_symbol = f"{symbol}.NS"
        
        print(f"\n[{i}/{len(stock_list)}] {symbol}...", end=" ")
        
        result = process_stock(symbol, yf_symbol)
        
        if result:
            results.append(result)
            successful += 1
        else:
            failed += 1
        
        # Rate limiting
        if i < len(stock_list):
            time.sleep(0.5)
    
    # Sort by score (highest first)
    results.sort(key=lambda x: x['total_score'], reverse=True)
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Total processed: {len(stock_list)}")
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    print(f"Success rate: {(successful/len(stock_list)*100):.1f}%")
    
    return results


def run_analysis(limit=5):
    """
    Function called by Flask server
    Processes 'limit' number of stocks and returns top 5 by score
    
    Args:
        limit: Number of stocks to process
    
    Returns:
        Top 5 stocks by score from the processed stocks
    """
    results = fetch_and_score_all_stocks(limit=limit)
    # Always return top 5 from processed stocks
    return results[:5]


def run_analysis_batched(limit=5):
    """
    Process all stocks in batches of 100 with 1-minute gaps between batches
    Then return top N by score
    
    This prevents NSE API rate limiting by taking breaks between batches
    
    Args:
        limit: Number of top stocks to return (default 5)
    
    Returns:
        Top N stocks by score from ALL processed stocks
    """
    print("="*60)
    print("STEP 1: Fetching NIFTY 500 stock list")
    print("="*60)
    
    stocks = get_nifty_500_stocks()
    stock_list = [s for s in stocks if s['symbol'] != 'NIFTY 500']
    
    print(f"✅ Got {len(stock_list)} stocks to process\n")
    
    all_results = []
    successful = 0
    failed = 0
    batch_size = 100
    
    for batch_num in range(0, len(stock_list), batch_size):
        batch_start = batch_num + 1
        batch_end = min(batch_num + batch_size, len(stock_list))
        batch = stock_list[batch_num:batch_end]
        
        print("\n" + "="*60)
        print(f"BATCH {batch_num//batch_size + 1}: Processing stocks {batch_start} to {batch_end}")
        print("="*60)
        
        # Process this batch
        for i, stock in enumerate(batch, batch_start):
            symbol = stock['symbol']
            yf_symbol = f"{symbol}.NS"
            
            print(f"\n[{i}/{len(stock_list)}] {symbol}...", end=" ")
            
            result = process_stock(symbol, yf_symbol)
            
            if result:
                all_results.append(result)
                successful += 1
            else:
                failed += 1
            
            # Rate limiting within batch
            time.sleep(0.5)
        
        # Wait 60 seconds before next batch (except for last batch)
        if batch_end < len(stock_list):
            print(f"\n\n⏸️  Batch {batch_num//batch_size + 1} complete. Waiting 60 seconds before next batch...")
            time.sleep(60)
    
    # Sort all results by score (highest first)
    all_results.sort(key=lambda x: x['total_score'], reverse=True)
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Total processed: {len(stock_list)}")
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    print(f"Success rate: {(successful/len(stock_list)*100):.1f}%")
    
    return all_results[:limit]


def display_top_stocks(results, top_n=10):
    """
    Display top N stocks with detailed scores
    
    Args:
        results: List of stock results
        top_n: Number of top stocks to display
    """
    print("\n" + "="*60)
    print(f"TOP {top_n} STOCKS BY SCORE")
    print("="*60)
    
    for i, stock in enumerate(results[:top_n], 1):
        print(f"\n{i}. {stock['symbol']}")
        print(f"   Price: ₹{stock['price']:.2f}")
        print(f"   Total Score: {stock['total_score']:.1f}/70")
        print(f"   └─ Volume: {stock['scores']['volume']:.0f}/100 (ratio: {stock['volume_ratio']:.2f}x)")
        print(f"   └─ RSI: {stock['scores']['rsi']:.0f}/100 (value: {stock['rsi']:.1f})")
        print(f"   └─ MACD: {stock['scores']['macd']:.0f}/100")
        print(f"   └─ EMA Trend: {stock['scores']['ema_trend']:.0f}/100")
        print(f"   └─ ADX: {stock['scores']['adx']:.0f}/100 (value: {stock['adx']:.1f})")


if __name__ == "__main__":
    print("\n🚀 Starting Complete Stock Analysis Pipeline...\n")
    
    # Process first 10 stocks for testing
    results = fetch_and_score_all_stocks(limit=10)
    
    # Display top 5
    if results:
        display_top_stocks(results, top_n=5)

