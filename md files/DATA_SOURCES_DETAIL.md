# Data Sources Breakdown - Clear List

## Overview
This document lists EXACTLY what data we fetch from each source and how we use it.

---

## SOURCE 1: Yahoo Finance (yfinance library)

### What We Fetch

#### 1. Daily OHLCV Data
For each stock in NIFTY 500:

| Parameter | Description | Example Value | How We Use It |
|-----------|-------------|---------------|---------------|
| **Date** | Trading date | 2026-01-10 | Index for all calculations |
| **Open** | Opening price | 2,450.50 | Entry price calculation |
| **High** | Highest price of day | 2,478.00 | Range calculation, volatility |
| **Low** | Lowest price of day | 2,442.00 | Range calculation, support levels |
| **Close** | Closing price | 2,465.00 | All indicators, signals |
| **Volume** | Number of shares traded | 5,234,567 | Volume analysis, liquidity check |
| **Adj Close** | Adjusted closing price | 2,465.00 | For historical accuracy (dividends/splits) |

#### Fetch Parameters
```python
import yfinance as yf

# For each stock
symbol = 'RELIANCE.NS'
start_date = '2025-11-12'  # 60 days back
end_date = '2026-01-10'    # Yesterday

data = yf.download(
    tickers=symbol,
    start=start_date,
    end=end_date,
    interval='1d',          # Daily data
    auto_adjust=False,      # We'll use Adj Close separately
    progress=False          # No progress bar
)

# Returns DataFrame with columns:
# Date (index), Open, High, Low, Close, Adj Close, Volume
```

#### What We Calculate From This Data

| Calculated Metric | Formula/Method | Used For |
|------------------|----------------|----------|
| **20 EMA** | Exponential moving average (20 days) | Trend identification, entry signals |
| **50 EMA** | Exponential moving average (50 days) | Trend confirmation |
| **RSI (14)** | Relative Strength Index | Momentum, overbought/oversold |
| **MACD** | 12-26-9 MACD | Trend momentum, crossovers |
| **ADX (14)** | Average Directional Index | Trend strength |
| **Volume MA (20)** | 20-day average volume | Volume breakout detection |
| **Volume Ratio** | Today's volume / 20-day avg | Scoring system (15% weight) |
| **Bollinger Bands** | 20-day SMA ± 2 std dev | Volatility, breakouts |
| **Price vs EMA** | Price position relative to EMAs | Scoring system (20% weight) |

#### Stock Symbol Format
- NSE stocks: Add `.NS` suffix
  - Example: `RELIANCE.NS`, `TCS.NS`, `INFY.NS`
- BSE stocks (fallback): Add `.BO` suffix
  - Example: `RELIANCE.BO`

#### Data Quality from yfinance
✅ **Good:**
- Reliable OHLCV data
- Free, no API key
- Historical data available
- Auto-adjusts for splits/dividends

❌ **Limitations:**
- Delayed data (~15-20 minutes)
- No Open Interest data
- No FII/DII data
- Sometimes missing data for small caps
- Rate limits (need delays between requests)

---

## SOURCE 2: NSE India Website (Web Scraping)

We fetch 4 different types of data from NSE:

---

### 2A. NIFTY 500 Stock List

#### URL
```
https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20500
```

#### What We Fetch

| Field | Description | Example | How We Use |
|-------|-------------|---------|------------|
| **symbol** | Stock symbol | RELIANCE | Primary identifier |
| **identifier** | Full identifier | RELIANCEEQN | Alternative ID |
| **open** | Day's open price | 2450.50 | Cross-check with yfinance |
| **dayHigh** | Day's high | 2478.00 | Validation |
| **dayLow** | Day's low | 2442.00 | Validation |
| **lastPrice** | Current/close price | 2465.00 | Latest price |
| **previousClose** | Previous day close | 2455.00 | Gap calculation |
| **pChange** | % change | 0.41 | Daily movement |
| **totalTradedVolume** | Volume | 5234567 | Liquidity check |
| **totalTradedValue** | Value in ₹ | 1287654321 | Liquidity check |
| **yearHigh** | 52-week high | 2950.00 | Breakout detection |
| **yearLow** | 52-week low | 2100.00 | Range context |
| **perChange365d** | 1-year % change | 15.5 | Momentum context |
| **perChange30d** | 1-month % change | 3.2 | Recent momentum |

#### Response Format
```json
{
  "data": [
    {
      "symbol": "RELIANCE",
      "open": 2450.50,
      "dayHigh": 2478.00,
      "dayLow": 2442.00,
      "lastPrice": 2465.00,
      "previousClose": 2455.00,
      "pChange": 0.41,
      "totalTradedVolume": 5234567,
      "totalTradedValue": 1287654321,
      "yearHigh": 2950.00,
      "yearLow": 2100.00,
      ...
    },
    ...
  ]
}
```

#### How Often to Fetch
- **Frequency:** Weekly
- **Purpose:** Get updated NIFTY 500 constituents (index rebalancing)
- **Save to:** `data/cache/NIFTY_500_stocks.csv`

---

### 2B. Open Interest Data (F&O Stocks)

#### URL (per stock)
```
https://www.nseindia.com/api/option-chain-equities?symbol=RELIANCE
```

#### What We Fetch

| Field | Description | Example | How We Use |
|-------|-------------|---------|------------|
| **underlyingValue** | Current stock price | 2465.00 | Price validation |
| **CE - openInterest** | Call option OI per strike | 1234567 | PCR calculation |
| **PE - openInterest** | Put option OI per strike | 2345678 | PCR calculation |
| **CE - changeinOpenInterest** | Change in Call OI | +12345 | OI change detection |
| **PE - changeinOpenInterest** | Change in Put OI | +23456 | OI change detection |
| **CE - totalTradedVolume** | Call volume | 567890 | Activity level |
| **PE - totalTradedVolume** | Put volume | 678901 | Activity level |
| **strikePrice** | Option strike price | 2500 | Price level context |

#### What We Calculate

| Metric | Formula | Used For |
|--------|---------|----------|
| **Total Call OI** | Sum of all call OI | PCR calculation |
| **Total Put OI** | Sum of all put OI | PCR calculation |
| **PCR (Put-Call Ratio)** | Total Put OI / Total Call OI | Sentiment (0.8-1.2 = healthy) |
| **OI Change** | Today's total OI - Yesterday's total OI | Buildup detection |
| **OI Change %** | (OI Change / Yesterday OI) × 100 | Scoring (10% weight) |
| **OI Pattern** | Price direction + OI direction | Long/Short buildup |

#### OI Patterns We Detect

| Pattern | Price | OI | Interpretation | Score |
|---------|-------|----|--------------------|-------|
| **Long Buildup** | ↑ | ↑ | Bulls adding positions (Bullish) | 100 |
| **Short Covering** | ↑ | ↓ | Bears exiting (Bullish short-term) | 50 |
| **Short Buildup** | ↓ | ↑ | Bears adding positions (Bearish) | 0 |
| **Long Unwinding** | ↓ | ↓ | Bulls exiting (Bearish) | 0 |

#### Response Format (Sample)
```json
{
  "records": {
    "data": [
      {
        "strikePrice": 2500,
        "expiryDate": "27-Feb-2026",
        "CE": {
          "strikePrice": 2500,
          "openInterest": 1234567,
          "changeinOpenInterest": 12345,
          "totalTradedVolume": 567890,
          "impliedVolatility": 18.5,
          "lastPrice": 45.50
        },
        "PE": {
          "strikePrice": 2500,
          "openInterest": 2345678,
          "changeinOpenInterest": 23456,
          "totalTradedVolume": 678901,
          "impliedVolatility": 19.2,
          "lastPrice": 32.75
        }
      },
      ...
    ],
    "underlyingValue": 2465.00
  }
}
```

#### Which Stocks Have OI Data
- Only F&O (Futures & Options) enabled stocks
- Approximately 200 stocks from NIFTY 500
- For non-F&O stocks: OI score = 50 (neutral)

#### How Often to Fetch
- **Frequency:** Daily (morning before market)
- **Save to:** `data/cache/oi_data/SYMBOL_OI.parquet`

---

### 2C. FII/DII Daily Activity Data

#### URL
```
https://www.nseindia.com/api/fiidiiTrading
```

#### What We Fetch

| Field | Description | Example | How We Use |
|-------|-------------|---------|------------|
| **date** | Trading date | 10-JAN-2026 | Date reference |
| **fii_buy_value** | FII buy value (₹ crores) | 8,234.56 | Market sentiment |
| **fii_sell_value** | FII sell value (₹ crores) | 7,123.45 | Market sentiment |
| **fii_net_value** | FII net (buy - sell) | +1,111.11 | Net institutional flow |
| **dii_buy_value** | DII buy value (₹ crores) | 5,678.90 | Domestic sentiment |
| **dii_sell_value** | DII sell value (₹ crores) | 4,567.89 | Domestic sentiment |
| **dii_net_value** | DII net (buy - sell) | +1,111.01 | Net domestic flow |

#### What We Calculate

| Metric | Formula | Used For |
|--------|---------|----------|
| **Total Institutional Flow** | FII net + DII net | Overall market sentiment |
| **3-day FII/DII trend** | Sum of last 3 days net | Short-term momentum |
| **5-day FII/DII trend** | Sum of last 5 days net | Swing trade momentum |

#### Response Format
```json
{
  "data": [
    {
      "date": "10-JAN-2026",
      "fii": {
        "buyValue": 8234.56,
        "sellValue": 7123.45,
        "netValue": 1111.11
      },
      "dii": {
        "buyValue": 5678.90,
        "sellValue": 4567.89,
        "netValue": 1111.01
      }
    }
  ]
}
```

#### Limitation
- This is **market-level data**, not stock-level
- For stock-level FII/DII, we need shareholding pattern (quarterly)

#### How Often to Fetch
- **Frequency:** Daily
- **Save to:** `data/cache/fii_dii/daily_activity.parquet`

---

### 2D. FII/DII Shareholding Pattern (Stock-Level)

#### URL (per stock)
```
https://www.nseindia.com/api/corporates-shareholding?index=equities&symbol=RELIANCE
```

#### What We Fetch

| Field | Description | Example | How We Use |
|-------|-------------|---------|------------|
| **date** | Quarter end date | 31-DEC-2025 | Period reference |
| **promoter_holding** | Promoter % | 50.39 | Ownership structure |
| **fii_holding** | FII % | 18.52 | Foreign institutional holding |
| **dii_holding** | DII % | 12.87 | Domestic institutional holding |
| **public_holding** | Retail/public % | 18.22 | Float |
| **total_shares** | Total shares outstanding | 6,766,257,103 | Market cap calculation |

#### What We Calculate for Scoring

| Metric | Formula | Weight | Used For |
|--------|---------|--------|----------|
| **FII % Change** | Current FII % - Previous Quarter FII % | - | Detect accumulation |
| **DII % Change** | Current DII % - Previous Quarter DII % | - | Detect accumulation |
| **Total Inst Change** | FII change + DII change | 20% | Main scoring metric |
| **3-day proxy** | Use daily market FII/DII × sector factor | 20% | Recent momentum |

#### Scoring Logic
```python
# Since shareholding is quarterly, we use a proxy:
# 1. Get quarterly change (from shareholding pattern)
# 2. Adjust by daily FII/DII market data for the sector
# 3. Score based on recent institutional activity

FII_DII_Score = 0

# Check if FII+DII % increased in last quarter
if (current_fii_pct - prev_quarter_fii_pct) > 0.5:
    FII_DII_Score += 50
elif (current_fii_pct - prev_quarter_fii_pct) > 0.2:
    FII_DII_Score += 30

# Adjust based on recent 5-day market FII/DII flow in sector
if sector_fii_dii_5day > 0 and net_flow_significant:
    FII_DII_Score += 50

# Final score: 0-100
```

#### Response Format
```json
{
  "data": [
    {
      "date": "31-DEC-2025",
      "shareholding": {
        "promoter": 50.39,
        "fii": 18.52,
        "dii": 12.87,
        "public": 18.22
      },
      "totalShares": 6766257103
    }
  ]
}
```

#### Challenge
- Updated only **quarterly** (every 3 months)
- Not real-time
- **Solution:** Combine with daily market FII/DII data as proxy

#### How Often to Fetch
- **Frequency:** Monthly (to catch quarterly updates)
- **Save to:** `data/cache/fii_dii/shareholding/SYMBOL.parquet`

---

## SOURCE 3: Calculated/Derived Data

These we calculate ourselves from the fetched data:

### From yfinance Data

| Indicator | Input | Library/Method | Output |
|-----------|-------|----------------|--------|
| **20 EMA** | Close prices | pandas `.ewm(span=20)` | Series |
| **50 EMA** | Close prices | pandas `.ewm(span=50)` | Series |
| **RSI (14)** | Close prices | `ta.momentum.RSIIndicator` | 0-100 value |
| **MACD (12,26,9)** | Close prices | `ta.trend.MACD` | MACD line, Signal line, Histogram |
| **ADX (14)** | High, Low, Close | `ta.trend.ADXIndicator` | 0-100 value |
| **BB (20,2)** | Close prices | `ta.volatility.BollingerBands` | Upper, Middle, Lower bands |
| **Volume MA** | Volume | pandas `.rolling(20).mean()` | Series |
| **ATR (14)** | High, Low, Close | `ta.volatility.AverageTrueRange` | Value (for stop-loss) |

### Technical Pattern Detection

| Pattern | Detection Logic | Used For |
|---------|-----------------|----------|
| **Higher Highs** | high[i] > high[i-5] > high[i-10] | Uptrend confirmation |
| **Higher Lows** | low[i] > low[i-5] > low[i-10] | Uptrend confirmation |
| **Consolidation** | (high - low) / close < 0.05 for 10+ days | Breakout setup |
| **Volume Breakout** | volume > 2 × volume_ma | Confirmation signal |
| **52-week High Breakout** | close > yearHigh × 0.98 | Momentum signal |

---

## Data Fetch Summary Table

| Data Type | Source | Update Frequency | Processing Time | Critical? |
|-----------|--------|------------------|-----------------|-----------|
| **OHLCV** | Yahoo Finance | Daily | 3-5 mins | ✅ Critical |
| **Stock List** | NSE | Weekly | 10 seconds | ✅ Critical |
| **Open Interest** | NSE | Daily | 10-15 mins | ⚠️ Important |
| **FII/DII Market** | NSE | Daily | 5 seconds | ⚠️ Important |
| **FII/DII Holdings** | NSE | Monthly | 2-3 mins | ⚠️ Important |
| **Technical Indicators** | Calculated | Real-time | 1-2 mins | ✅ Critical |

---

## Complete Data Flow

```
Morning 8:00 AM
    ↓
[1] Fetch NIFTY 500 List (NSE)
    → 500 stock symbols with basic info
    ↓
[2] Fetch OHLCV (Yahoo Finance)
    → Open, High, Low, Close, Volume (60 days)
    → For all 500 stocks
    ↓
[3] Calculate Technical Indicators
    → EMA, RSI, MACD, ADX, Volume MA
    → From OHLCV data
    ↓
[4] Fetch OI Data (NSE - F&O stocks only)
    → Open Interest, PCR
    → Detect long/short buildup
    ↓
[5] Fetch FII/DII Data (NSE)
    → Daily market activity
    → Quarterly shareholding
    → Combine for stock-level proxy
    ↓
[6] Scoring System
    → Combine all factors
    → Weight-based scoring (0-100)
    ↓
8:30 AM - Top 10 Stocks Ready!
```

---

## Data Storage Format

```
data/
├── cache/
│   ├── nifty_500_stocks.csv          # 500 stocks list from NSE
│   │   Columns: symbol, name, sector, market_cap, is_fno
│   │
│   ├── price_data/
│   │   ├── RELIANCE.NS.parquet       # OHLCV + indicators
│   │   │   Columns: date, open, high, low, close, volume,
│   │   │            ema_20, ema_50, rsi, macd, macd_signal,
│   │   │            adx, volume_ma, bb_upper, bb_lower
│   │   └── ... (500 files)
│   │
│   ├── oi_data/
│   │   ├── RELIANCE_OI.parquet       # Daily OI summary
│   │   │   Columns: date, total_call_oi, total_put_oi, pcr,
│   │   │            oi_change, oi_change_pct, pattern
│   │   └── ... (200 F&O stocks)
│   │
│   └── fii_dii/
│       ├── market_activity.parquet   # Daily market-level
│       │   Columns: date, fii_net, dii_net, total_net
│       │
│       └── holdings/
│           ├── RELIANCE.parquet      # Quarterly holdings
│           │   Columns: date, fii_pct, dii_pct, 
│           │            fii_change, dii_change
│           └── ... (500 files)
```

---

## Next Steps

With this clear data structure:
1. ✅ We know exactly what to fetch
2. ✅ We know from which source
3. ✅ We know how to use each data point
4. ✅ We know how to store it

**Ready to start implementing the data fetcher?**

