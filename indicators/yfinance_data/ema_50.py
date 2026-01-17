"""
50-day EMA Calculator
"""
import pandas as pd

def calculate_ema_50(df):
    """
    Calculate 50-day Exponential Moving Average
    """
    if df is None or df.empty:
        return df
    
    df['ema_50'] = df['Close'].ewm(span=50, adjust=False).mean()
    return df
