# Yahoo Finance - Data to Fetch

## Stock Symbol Format
- NSE stocks: `SYMBOL.NS` (e.g., RELIANCE.NS)

## Data Points We Fetch

For each stock in NIFTY 500:

1. Date
2. Open
3. High
4. Low
5. Close
6. Volume
7. Adj Close

## Time Period
- Daily screening: Last 60 days
- Backtesting: Last 2 years

---

## Days Required for Each Indicator

| Indicator | Weight | Days Needed | Why |
|-----------|--------|-------------|-----|
| **Volume** | 15% | 20 days | Need 20-day average volume |
| **MACD** | 13% | 35 days | Uses 26-day EMA + warmup |
| **RSI** | 12% | 20 days | Uses 14-day period + warmup |
| **50 EMA** | 20% | 60 days | Need 50 days + warmup |
| **20 EMA** | 20% | 30 days | Need 20 days + warmup |
| **ADX** | 10% | 20 days | Uses 14-day period + warmup |

**Minimum Required:** 60 days (covers all indicators with warmup period)

## That's it.

