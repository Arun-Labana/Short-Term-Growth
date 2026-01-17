"""
Scoring Module
Converts indicator values to 0-100 scores and calculates weighted total
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.scoring_config import (
    WEIGHTS,
    VOLUME_THRESHOLDS,
    MACD_THRESHOLDS,
    RSI_THRESHOLDS,
    TREND_EMA_THRESHOLDS,
    ADX_THRESHOLDS,
    OI_PATTERN_SCORES
)

def score_volume(volume_ratio):
    """Score volume ratio (0-100)"""
    if volume_ratio is None:
        return 0
    
    if volume_ratio >= VOLUME_THRESHOLDS['excellent']['min']:
        return VOLUME_THRESHOLDS['excellent']['score']
    elif volume_ratio >= VOLUME_THRESHOLDS['very_good']['min']:
        return VOLUME_THRESHOLDS['very_good']['score']
    elif volume_ratio >= VOLUME_THRESHOLDS['good']['min']:
        return VOLUME_THRESHOLDS['good']['score']
    elif volume_ratio >= VOLUME_THRESHOLDS['moderate']['min']:
        return VOLUME_THRESHOLDS['moderate']['score']
    else:
        return VOLUME_THRESHOLDS['low']['score']

def score_macd(macd, signal, histogram):
    """Score MACD (0-100)"""
    if macd is None or signal is None or histogram is None:
        return 0
    
    macd_above_signal = macd > signal
    
    if histogram > 0 and macd_above_signal:
        return MACD_THRESHOLDS['strong_bullish']['score']
    elif histogram > 0:
        return MACD_THRESHOLDS['bullish']['score']
    elif macd_above_signal:
        return MACD_THRESHOLDS['weak_bullish']['score']
    else:
        return MACD_THRESHOLDS['bearish']['score']

def score_rsi(rsi):
    """Score RSI (0-100) - Optimized for 5-7 day swing trades"""
    if rsi is None:
        return 0
    
    if rsi >= 75:
        return RSI_THRESHOLDS['very_overbought']['score']
    elif rsi >= 70:
        return RSI_THRESHOLDS['strong']['score']
    elif rsi >= 55:
        return RSI_THRESHOLDS['perfect']['score']
    elif rsi >= 50:
        return RSI_THRESHOLDS['building']['score']
    elif rsi >= 45:
        return RSI_THRESHOLDS['neutral']['score']
    elif rsi >= 40:
        return RSI_THRESHOLDS['weak']['score']
    else:
        return RSI_THRESHOLDS['too_weak']['score']

def score_trend_ema(current_price, ema_20, ema_50):
    """Score trend/EMA positioning (0-100)"""
    if current_price is None or ema_20 is None or ema_50 is None:
        return 0
    
    above_20 = current_price > ema_20
    above_50 = current_price > ema_50
    ema20_above_ema50 = ema_20 > ema_50
    
    if above_20 and above_50 and ema20_above_ema50:
        # Calculate distance percentage from 20 EMA
        distance_pct = ((current_price - ema_20) / ema_20) * 100
        if distance_pct >= 2:
            return TREND_EMA_THRESHOLDS['above_both_strong']['score']
        else:
            return TREND_EMA_THRESHOLDS['above_both_moderate']['score']
    elif above_20 and not above_50:
        return TREND_EMA_THRESHOLDS['above_20_only']['score']
    elif not above_20 and above_50:
        return TREND_EMA_THRESHOLDS['between']['score']
    else:
        return TREND_EMA_THRESHOLDS['below_both']['score']

def score_adx(adx):
    """Score ADX (0-100)"""
    if adx is None:
        return 0
    
    if adx >= 40:
        return ADX_THRESHOLDS['very_strong']['score']
    elif adx >= 25:
        return ADX_THRESHOLDS['strong']['score']
    elif adx >= 20:
        return ADX_THRESHOLDS['moderate']['score']
    else:
        return ADX_THRESHOLDS['weak']['score']

def score_oi_pattern(oi_pattern):
    """Score Open Interest pattern (0-100)"""
    if oi_pattern is None or oi_pattern not in OI_PATTERN_SCORES:
        return OI_PATTERN_SCORES['no_pattern']
    
    return OI_PATTERN_SCORES[oi_pattern]

def calculate_total_score(scores):
    """
    Calculate weighted total score
    scores: dict with keys matching WEIGHTS keys
    """
    total = 0
    for factor, weight in WEIGHTS.items():
        if factor in scores and scores[factor] is not None:
            total += (scores[factor] * weight / 100)
    
    return round(total, 2)

def score_stock(df, oi_pattern=None):
    """
    Score a stock based on calculated indicators in dataframe
    Returns dict with individual scores and total
    """
    if df is None or df.empty:
        return None
    
    latest = df.iloc[-1]
    
    # Get indicator values
    volume_ratio = latest.get('volume_ratio')
    macd = latest.get('macd')
    macd_signal = latest.get('macd_signal')
    macd_hist = latest.get('macd_hist')
    rsi = latest.get('rsi')
    ema_20 = latest.get('ema_20')
    ema_50 = latest.get('ema_50')
    adx = latest.get('adx')
    current_price = latest['Close']
    
    # Calculate scores
    volume_score = score_volume(volume_ratio)
    macd_score = score_macd(macd, macd_signal, macd_hist)
    rsi_score = score_rsi(rsi)
    trend_score = score_trend_ema(current_price, ema_20, ema_50)
    adx_score = score_adx(adx)
    oi_score = score_oi_pattern(oi_pattern)
    
    scores = {
        'volume': volume_score,
        'macd': macd_score,
        'rsi': rsi_score,
        'ema_trend': trend_score,
        'adx': adx_score,
        'oi_pattern': oi_score
    }
    
    scores['total'] = calculate_total_score(scores)
    
    return scores
