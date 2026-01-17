"""
20-day EMA Calculator
"""
import pandas as pd

def calculate_ema_20(df):
    """
    Calculate 20-day Exponential Moving Average
    """
    if df is None or df.empty:
        return df
    
    df['ema_20'] = df['Close'].ewm(span=20, adjust=False).mean()
    return df
