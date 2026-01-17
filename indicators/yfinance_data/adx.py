"""
ADX Calculator
Calculates Average Directional Index
"""
import pandas as pd

def calculate_adx(df, period=14):
    """
    Calculate ADX (Average Directional Index)
    Measures trend strength
    """
    if df is None or df.empty or len(df) < period + 1:
        return None
    
    # Calculate True Range (TR)
    df['H-L'] = df['High'] - df['Low']
    df['H-PC'] = abs(df['High'] - df['Close'].shift(1))
    df['L-PC'] = abs(df['Low'] - df['Close'].shift(1))
    df['TR'] = df[['H-L', 'H-PC', 'L-PC']].max(axis=1)
    
    # Calculate Directional Movement
    df['DMplus'] = 0.0
    df['DMminus'] = 0.0
    
    df.loc[(df['High'] - df['High'].shift(1)) > (df['Low'].shift(1) - df['Low']), 'DMplus'] = df['High'] - df['High'].shift(1)
    df.loc[(df['Low'].shift(1) - df['Low']) > (df['High'] - df['High'].shift(1)), 'DMminus'] = df['Low'].shift(1) - df['Low']
    
    df['DMplus'] = df['DMplus'].clip(lower=0)
    df['DMminus'] = df['DMminus'].clip(lower=0)
    
    # Calculate Smoothed TR and DM
    df['TR_smooth'] = df['TR'].rolling(window=period).sum()
    df['DMplus_smooth'] = df['DMplus'].rolling(window=period).sum()
    df['DMminus_smooth'] = df['DMminus'].rolling(window=period).sum()
    
    # Calculate Directional Indicators
    df['DIplus'] = 100 * (df['DMplus_smooth'] / df['TR_smooth'])
    df['DIminus'] = 100 * (df['DMminus_smooth'] / df['TR_smooth'])
    
    # Calculate DX
    df['DX'] = 100 * abs(df['DIplus'] - df['DIminus']) / (df['DIplus'] + df['DIminus'])
    
    # Calculate ADX
    df['adx'] = df['DX'].rolling(window=period).mean()
    
    return df
