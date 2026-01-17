# Simple Trading Screener - Project Plan

## Goal
Daily screener that finds top 10 stocks for swing trading (3-7 days, 3-5% target)

---

## What We're Looking For

### ✅ BUY Signals (Must have most of these)

**Trend:**
- Price > 20 EMA
- Price > 50 EMA
- Higher highs + higher lows pattern

**Volume:**
- Volume > 2x average
- Rising volume on green candles

**Patterns:**
- Consolidation breakout
- Flag & pole
- Cup & handle
- Pullback to 20 EMA in uptrend

**Indicators:**
- RSI between 55-70 (strong, not overheated)
- MACD fresh bullish crossover
- ADX > 20 (trending)

**F&O Data:**
- Long buildup: Price ↑ + OI ↑
- Short covering: Price ↑ + OI ↓
- PCR between 0.8-1.2 (healthy)

**FII/DII:**
- Net buyers in the sector
- Positive institutional flow

### ❌ AVOID Signals

- RSI > 75 (overextended)
- Low volume
- Price below 50 DMA
- PCR > 1.3 (overbought risk)

---

## Weight-Based Scoring System

**Formula:** `Final Score = Σ (Weight × Factor Score)`

Each factor gets scored 0-100, then multiplied by its weight.

### Weights Distribution

| Factor | Weight | How to Score (0-100) |
|--------|--------|---------------------|
| **FII/DII Flow** | **20%** | Based on net buying intensity |
| **Volume** | **15%** | Volume ratio vs average (higher = better) |
| **MACD** | **13%** | Crossover strength and histogram |
| **RSI** | **12%** | Sweet spot scoring (55-70 = max score) |
| **Trend (EMA)** | **20%** | Price vs 20/50 EMA alignment |
| **ADX** | **10%** | Trend strength (>20 = trending) |
| **OI Buildup** | **10%** | Long buildup strength |

**Total: 100%**

### Detailed Scoring Logic

**1. FII/DII Flow (20%):**
Score based on **change in FII+DII holding percentage** (comparing last 2-3 days):

**Logic:** Compare FII/DII % today vs 3 days ago
- FII % today = (FII shares / Total shares) × 100
- Change = FII % today - FII % 3 days ago

**Scoring:**
- 100: FII+DII % increased by >0.5% (strong accumulation)
- 80: Increased by 0.3-0.5% (good accumulation)
- 60: Increased by 0.1-0.3% (mild accumulation)
- 40: Increased by 0-0.1% (neutral/slight increase)
- 20: Decreased by 0-0.2% (mild selling)
- 0: Decreased by >0.2% (active selling)

**Example:**
- Stock ABC: FII holding was 18.5% (3 days ago), now 19.2% = +0.7% increase = Score 100 ✅
- Stock XYZ: FII holding was 22.0% (3 days ago), now 21.6% = -0.4% decrease = Score 0 ❌

**Data Source:** NSE shareholding pattern (updated quarterly) + daily FII/DII data from NSE

**Note:** We're looking for **momentum in institutional accumulation**, not just absolute holdings. Rising FII/DII % = smart money entering = bullish signal!

**2. Volume (15%):**
- Volume ratio = Today's volume / 20-day avg volume
- Score = min(100, ratio × 50)
- Example: 2x volume = 100 score, 1.5x = 75 score

**3. MACD (13%):**
- 100: Fresh bullish crossover (last 1-3 days) + positive histogram
- 75: Bullish crossover 4-7 days ago
- 50: MACD > Signal line but old crossover
- 0: Bearish crossover

**4. RSI (12%):** - 14-day RSI optimized for 5-7 day swing trades
- 100: RSI 55-70 → Perfect entry (momentum + room to grow)
- 85: RSI 50-55 → Building momentum (good entry)
- 60: RSI 70-75 → Overbought risk (cautious)
- 50: RSI 45-50 → Neutral (wait for better setup)
- 25: RSI 40-45 → Weak momentum (avoid)
- 0: RSI >75 → Very overbought (avoid completely)
- 0: RSI <40 → Too weak for swing trades (avoid)

**5. Trend - EMA Alignment (20%):**
- 100: Price > 20 EMA > 50 EMA (perfect alignment)
- 75: Price > 20 EMA but 20 < 50 EMA
- 50: Price > 20 EMA only
- 25: Price between 20 and 50 EMA
- 0: Price < both EMAs

**6. ADX (10%):**
- 100: ADX > 30 (strong trend)
- 75: ADX 25-30
- 50: ADX 20-25
- 0: ADX < 20 (no trend)

**7. OI Buildup (10%):**
- 100: Price ↑ + OI ↑ >15% (strong long buildup)
- 75: Price ↑ + OI ↑ 10-15%
- 50: Price ↑ + OI ↑ 5-10%
- 25: Price ↑ + OI ↓ (short covering - okay but weaker)
- 0: Other combinations

### Example Calculation

```
Stock: RELIANCE

FII/DII Flow:     80/100 × 0.20 = 16.0
Volume:           100/100 × 0.15 = 15.0
MACD:             100/100 × 0.13 = 13.0
RSI:              90/100 × 0.12 = 10.8
Trend (EMA):      100/100 × 0.20 = 20.0
ADX:              75/100 × 0.10 = 7.5
OI Buildup:       75/100 × 0.10 = 7.5
                          ─────────────
Final Score:                     89.8/100
```

**Top 10 = Stocks with highest final scores (typically >70)**

Top 10 highest scoring stocks = Daily picks

---

## Implementation (4 Weeks)

### Week 1: Data + Basic Indicators
- Get NSE stock list
- Fetch daily OHLCV data (yfinance)
- Calculate: 20 EMA, 50 EMA, Volume avg
- Calculate: RSI, MACD, ADX
- Test with 20 stocks

### Week 2: OI + FII/DII Data
- Scrape OI data from NSE
- Get FII/DII data from NSE
- Detect long buildup, short covering
- PCR calculation

### Week 3: Screening + Scoring
- Apply filters (avoid conditions)
- Calculate score for each stock
- Rank and get top 10
- Show: Entry, Target (+4%), Stop-loss (-2%)

### Week 4: Backtesting
- Test last 1 year
- Check: Win rate, avg return, max loss
- Adjust if needed
- Ready to use

---

## Daily Workflow

**Morning (8:00 AM):**
1. Run screener
2. Get top 10 stocks
3. Review manually
4. Pick 3-5 stocks
5. Place orders at 9:15 AM

**Output Format:**
```
Stock: RELIANCE
Score: 85/100
Price: 2,450
Entry: 2,460 (at open)
Target: 2,560 (4% gain)
Stop: 2,410 (2% loss)
Signals: Price>EMA, Volume 2.5x, RSI 62, MACD cross, Long buildup
```

---

## File Structure

```
short-term-growth/
├── data_fetcher.py       # Get stock data
├── indicators.py         # Calculate EMA, RSI, MACD, ADX
├── oi_scraper.py         # NSE OI data
├── fii_dii_scraper.py    # FII/DII data
├── screener.py           # Main screening logic
├── backtester.py         # Test strategy
├── main.py               # Run daily
└── requirements.txt      # Python packages
```

---

## Risk Management (Built-in)

- Max 2% stop-loss
- 4% target = 1:2 risk-reward
- Max 5 positions at a time
- Position size calculator based on stop-loss

---

## Key Libraries

```
yfinance - Stock data
pandas - Data handling
ta - Technical indicators (RSI, MACD, ADX, EMA)
requests - NSE scraping
beautifulsoup4 - HTML parsing
```

---

## Success = Simple System That Works

- Runs every morning without issues
- Top 10 list in 15 minutes
- Win rate > 55%
- Easy to understand why stock was picked

**Keep it simple. Let data decide.**

