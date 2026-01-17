"""
Scoring Configuration
All weights and thresholds for stock scoring
"""

# Weights for each factor (must sum to 100)
WEIGHTS = {
    'volume': 15,
    'macd': 13,
    'rsi': 12,
    'trend_ema': 20,
    'adx': 10,
    'oi_pattern': 10,
    'fii_dii': 20  # Not implemented yet
}

# Volume Scoring Thresholds
VOLUME_THRESHOLDS = {
    'excellent': {'min': 2.0, 'score': 100},      # 2x+ volume
    'very_good': {'min': 1.5, 'max': 2.0, 'score': 80},
    'good': {'min': 1.2, 'max': 1.5, 'score': 60},
    'moderate': {'min': 1.0, 'max': 1.2, 'score': 40},
    'low': {'max': 1.0, 'score': 20}
}

# MACD Scoring Thresholds
MACD_THRESHOLDS = {
    'strong_bullish': {'hist_min': 0, 'macd_above_signal': True, 'score': 100},
    'bullish': {'hist_min': 0, 'macd_above_signal': False, 'score': 70},
    'weak_bullish': {'hist_max': 0, 'macd_above_signal': True, 'score': 40},
    'bearish': {'hist_max': 0, 'macd_above_signal': False, 'score': 10}
}

# RSI Scoring (14-day RSI optimized for 5-7 day swing trades)
RSI_THRESHOLDS = {
    'perfect': {'min': 55, 'max': 70, 'score': 100},      # Perfect entry (momentum + room to grow)
    'building': {'min': 50, 'max': 55, 'score': 85},      # Building momentum (good entry)
    'strong': {'min': 70, 'max': 75, 'score': 60},        # Overbought risk (cautious)
    'neutral': {'min': 45, 'max': 50, 'score': 50},       # Neutral (wait for better setup)
    'weak': {'min': 40, 'max': 45, 'score': 25},          # Weak momentum (avoid)
    'very_overbought': {'min': 75, 'score': 0},           # Very overbought (avoid completely)
    'too_weak': {'max': 40, 'score': 0}                   # Too weak for swing trades (avoid)
}

# Trend/EMA Scoring Thresholds
TREND_EMA_THRESHOLDS = {
    'above_both_strong': {'above_20': True, 'above_50': True, 'ema20_above_ema50': True, 'min_distance': 2, 'score': 100},
    'above_both_moderate': {'above_20': True, 'above_50': True, 'ema20_above_ema50': True, 'score': 80},
    'above_20_only': {'above_20': True, 'above_50': False, 'score': 50},
    'between': {'above_20': False, 'above_50': True, 'score': 30},
    'below_both': {'above_20': False, 'above_50': False, 'score': 0}
}

# ADX Scoring Thresholds
ADX_THRESHOLDS = {
    'very_strong': {'min': 40, 'score': 100},
    'strong': {'min': 25, 'max': 40, 'score': 80},
    'moderate': {'min': 20, 'max': 25, 'score': 60},
    'weak': {'max': 20, 'score': 30}
}

# OI Pattern Scoring
OI_PATTERN_SCORES = {
    'long_buildup': 100,      # Price ↑ + OI ↑ (Best for swing trades)
    'short_covering': 80,     # Price ↑ + OI ↓ (Good momentum)
    'long_unwinding': 20,     # Price ↓ + OI ↓ (Avoid)
    'short_buildup': 10,      # Price ↓ + OI ↑ (Bearish, avoid)
    'no_pattern': 40          # No clear pattern or no F&O data
}
