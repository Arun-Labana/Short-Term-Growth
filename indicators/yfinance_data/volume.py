"""
Calculate 20-day Volume Moving Average
"""

import pandas as pd


def calculate_volume_ma(df, period=20):
    """
    Calculate 20-day volume moving average
    
    Args:
        df: DataFrame with Volume column
        period: Moving average period (default: 20)
    
    Returns:
        DataFrame with volume_ma and volume_ratio columns
    """
    
    # Calculate 20-day volume moving average
    df['volume_ma'] = df['Volume'].rolling(window=period).mean()
    
    # Calculate volume ratio (current volume / average volume)
    df['volume_ratio'] = df['Volume'] / df['volume_ma']
    
    return df


def calculate_volume_ratio(df, period=20):
    """
    Calculate volume ratio for the latest day
    """
    if df is None or df.empty or len(df) < period:
        return None
    
    volume_ma = df['Volume'].rolling(window=period).mean()
    latest_volume = df['Volume'].iloc[-1]
    latest_ma = volume_ma.iloc[-1]
    
    if latest_ma == 0 or pd.isna(latest_ma):
        return None
    
    return latest_volume / latest_ma


if __name__ == "__main__":
    print("Volume MA Calculator - Ready")
