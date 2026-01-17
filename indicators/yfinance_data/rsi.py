"""
RSI Calculator
Calculates 14-day Relative Strength Index
"""
import pandas as pd

def calculate_rsi(df, period=14):
    """
    Calculate RSI (Relative Strength Index)
    """
    if df is None or df.empty:
        return df
    
    # Calculate price changes
    delta = df['Close'].diff()
    
    # Separate gains and losses
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    # Calculate average gain and loss
    avg_gain = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.rolling(window=period, min_periods=period).mean()
    
    # Calculate RS and RSI
    rs = avg_gain / avg_loss
    df['rsi'] = 100 - (100 / (1 + rs))
    
    return df
