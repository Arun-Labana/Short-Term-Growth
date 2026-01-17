"""
MACD Calculator
Calculates MACD, Signal Line, and Histogram
"""
import pandas as pd

def calculate_macd(df):
    """
    Calculate MACD indicator
    MACD = 12-day EMA - 26-day EMA
    Signal = 9-day EMA of MACD
    Histogram = MACD - Signal
    """
    if df is None or df.empty:
        return df
    
    # Calculate 12-day and 26-day EMAs
    ema_12 = df['Close'].ewm(span=12, adjust=False).mean()
    ema_26 = df['Close'].ewm(span=26, adjust=False).mean()
    
    # MACD Line
    df['macd'] = ema_12 - ema_26
    
    # Signal Line (9-day EMA of MACD)
    df['macd_signal'] = df['macd'].ewm(span=9, adjust=False).mean()
    
    # Histogram
    df['macd_hist'] = df['macd'] - df['macd_signal']
    
    return df
