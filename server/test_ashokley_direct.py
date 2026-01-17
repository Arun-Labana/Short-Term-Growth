"""
Test script to directly calculate ASHOKLEY score without calling API
For debugging deterministic scoring
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api_requests.yfinance_stock_data import fetch_stock_data
from api_requests.nselib_oi_fetcher import get_oi_data
from indicators.yfinance_data.volume import calculate_volume_ratio
from indicators.yfinance_data.macd import calculate_macd
from indicators.yfinance_data.rsi import calculate_rsi
from indicators.yfinance_data.ema_20 import calculate_ema_20
from indicators.yfinance_data.ema_50 import calculate_ema_50
from indicators.yfinance_data.adx import calculate_adx
from indicators.scorer import *

def test_ashokley_direct():
    """Directly calculate ASHOKLEY score"""
    symbol = "ASHOKLEY"
    
    print(f"\nCalculating score for {symbol}...")
    print("="*80)
    
    # Fetch data
    df = fetch_stock_data(symbol)
    if df is None or df.empty:
        print(f"No data for {symbol}")
        return
    
    # Get OI data
    oi_pattern = get_oi_data(symbol.replace('.NS', ''))
    
    # Calculate indicators
    volume_ratio = calculate_volume_ratio(df)
    macd, signal, histogram = calculate_macd(df)
    rsi = calculate_rsi(df)
    ema_20 = calculate_ema_20(df)
    ema_50 = calculate_ema_50(df)
    adx = calculate_adx(df)
    current_price = df['Close'].iloc[-1]
    
    # Calculate scores
    volume_score = score_volume(volume_ratio)
    macd_score = score_macd(macd, signal, histogram)
    rsi_score = score_rsi(rsi)
    trend_ema_score = score_trend_ema(current_price, ema_20, ema_50)
    adx_score = score_adx(adx)
    oi_pattern_score = score_oi_pattern(oi_pattern)
    
    scores = {
        'volume': volume_score,
        'macd': macd_score,
        'rsi': rsi_score,
        'trend_ema': trend_ema_score,
        'adx': adx_score,
        'oi_pattern': oi_pattern_score
    }
    
    total_score = calculate_total_score(scores)
    
    print(f"\n{symbol} Analysis:")
    print(f"  Current Price: {current_price:.2f}")
    print(f"  Volume Ratio: {volume_ratio:.2f} → Score: {volume_score}")
    print(f"  MACD: {macd:.2f}, Signal: {signal:.2f}, Hist: {histogram:.2f} → Score: {macd_score}")
    print(f"  RSI: {rsi:.2f} → Score: {rsi_score}")
    print(f"  20 EMA: {ema_20:.2f}, 50 EMA: {ema_50:.2f} → Score: {trend_ema_score}")
    print(f"  ADX: {adx:.2f} → Score: {adx_score}")
    print(f"  OI Pattern: {oi_pattern} → Score: {oi_pattern_score}")
    print(f"\n  TOTAL SCORE: {total_score}")
    print("="*80)

if __name__ == '__main__':
    test_ashokley_direct()
