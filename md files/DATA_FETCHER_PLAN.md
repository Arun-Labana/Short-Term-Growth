# Data Fetcher - Detailed Plan

## Overview
The data fetcher is responsible for collecting all required data from various sources, managing date ranges, caching, and ensuring data quality.

---

## 1. Data Requirements

### A. Price Data (OHLCV)
**What we need:**
- Open, High, Low, Close, Volume
- Daily timeframe
- **For NIFTY 500 stocks (~500 stocks)** - most liquid and reliable

**Lookback Period:**
- **For Daily Screening:** Last 60 days (enough for 50 EMA + indicators)
- **For Backtesting:** Last 2 years (500+ trading days)

**Why NIFTY 500?**
- Covers ~95% of market capitalization
- High liquidity = better execution
- Better data quality
- Faster processing (~500 vs ~2000 stocks)
- Still comprehensive market coverage

### B. Technical Indicators (Calculated from price data)
- 20 EMA, 50 EMA
- RSI (14)
- MACD (12, 26, 9)
- ADX (14)
- Volume moving average (20 days)

### C. Open Interest Data
**What we need:**
- Daily OI for F&O stocks (~200 stocks)
- OI change (today vs yesterday)
- Strike-wise OI for PCR calculation

**Lookback:** Last 5-10 days

### D. FII/DII Data
**What we need:**
- FII holding % in each stock
- DII holding % in each stock
- Change over last 3 days

**Challenge:** This data is updated quarterly (shareholding pattern)
**Solution:** Use daily FII/DII market-level data as proxy + sector-wise breakup

### E. Stock Universe
**What we need:**
- **List of NIFTY 500 stocks (~500 stocks)**
- Stock name, symbol, sector, market cap
- F&O enabled flag
- Updated weekly from NSE

---

## 2. Data Sources

### Source 1: Yahoo Finance (via yfinance)
**Pros:**
- Free and reliable
- Good historical OHLCV data
- Easy to use Python library
- No API key needed

**Cons:**
- No OI data
- No FII/DII data
- Rate limits (pause between requests)
- Some NSE stocks have data quality issues

**What we'll fetch:**
- Daily OHLCV for all NSE stocks
- Symbol format: `RELIANCE.NS` (NSE), `RELIANCE.BO` (BSE)

**Usage:**
```python
import yfinance as yf
data = yf.download('RELIANCE.NS', start='2024-01-01', end='2026-01-11')
```

### Source 2: NSE India Website (Web Scraping)
**Pros:**
- Official source
- Has OI data, FII/DII data
- Free

**Cons:**
- Rate limiting (aggressive)
- Need to handle cookies/sessions
- Website structure can change
- Need to respect robots.txt

**What we'll fetch:**
1. **Stock List (NIFTY 500):**
   - URL: `https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20500`
   - Get all 500 stocks with name, symbol, sector, market cap
   - Update weekly to catch index rebalancing

2. **OI Data:**
   - URL: `https://www.nseindia.com/api/option-chain-equities?symbol=RELIANCE`
   - Daily OI, strike-wise data

3. **FII/DII Data:**
   - URL: `https://www.nseindia.com/api/fiidiiTrading`
   - Market-level FII/DII daily data
   - Participant-wise data

4. **Shareholding Pattern:**
   - URL: `https://www.nseindia.com/api/corporates-financial-results?index=equities`
   - Quarterly FII/DII holding % per stock

### Source 3: Alternative APIs (Backup)
**If NSE scraping fails:**
- **Alpha Vantage** (limited free tier)
- **Upstox API** (requires account)
- **Zerodha Kite API** (requires account)
- **Financial Modeling Prep** (paid)

---

## 3. Date Management Logic

### A. Determining Date Ranges

**For Daily Screening (Morning Run):**
```python
from datetime import datetime, timedelta

# Fetch data from (today - 60 days) to yesterday
end_date = datetime.now() - timedelta(days=1)  # Yesterday
start_date = end_date - timedelta(days=60)     # 60 days back

# Adjust for weekends/holidays
# If today is Monday, yesterday is Friday's data (already handled)
```

**For Backtesting:**
```python
# User specifies backtest period
backtest_start = '2024-01-01'
backtest_end = '2026-01-10'

# But fetch extra 60 days before start for indicator calculation
data_fetch_start = backtest_start - timedelta(days=60)
```

**Handling Market Holidays:**
- Maintain a list of NSE holidays
- Skip those dates in data fetching
- Or let yfinance handle it (returns only trading days)

### B. Incremental Updates

**Strategy:** Don't fetch all data every day

```
Day 1 (First Run):
├── Fetch last 60 days for NIFTY 500 stocks
├── Store in cache
└── Takes ~15-25 minutes (500 stocks)

Day 2 (Subsequent Runs):
├── Check cache for existing data
├── Fetch only yesterday's data (1 day)
├── Append to cache
└── Takes ~3-5 minutes
```

**Implementation:**
```python
def get_required_dates(symbol, lookback_days=60):
    # Check what we have in cache
    cached_data = load_from_cache(symbol)
    
    if cached_data is None:
        # No cache - fetch full lookback
        start_date = today - timedelta(days=lookback_days)
        end_date = yesterday
    else:
        # Have cache - fetch only missing dates
        last_cached_date = cached_data.index[-1]
        start_date = last_cached_date + timedelta(days=1)
        end_date = yesterday
    
    return start_date, end_date
```

---

## 4. Data Fetcher Architecture

### File Structure
```
data_fetcher/
├── __init__.py
├── base_fetcher.py           # Base class for all fetchers
├── yfinance_fetcher.py        # Yahoo Finance data
├── nse_scraper.py             # NSE website scraping
├── oi_fetcher.py              # Open Interest data
├── fii_dii_fetcher.py         # FII/DII data
├── stock_universe.py          # Get list of all NSE stocks
└── cache_manager.py           # Handle data caching
```

### Core Classes

**1. BaseFetcher (Abstract Class)**
```python
class BaseFetcher:
    def fetch(self, symbol, start_date, end_date):
        """Fetch data for a symbol between dates"""
        pass
    
    def validate_data(self, df):
        """Check if data is valid"""
        pass
    
    def handle_errors(self, error):
        """Error handling logic"""
        pass
```

**2. YFinanceFetcher**
```python
class YFinanceFetcher(BaseFetcher):
    def fetch_single(self, symbol, start, end):
        """Fetch data for one stock"""
        
    def fetch_batch(self, symbols, start, end):
        """Fetch data for multiple stocks (parallel)"""
        
    def retry_failed(self, failed_symbols):
        """Retry failed downloads"""
```

**3. NSEScraper**
```python
class NSEScraper(BaseFetcher):
    def __init__(self):
        self.session = requests.Session()
        self.headers = self._get_headers()
        self.cookies = self._get_cookies()
    
    def fetch_stock_list(self):
        """Get all NSE stocks"""
    
    def fetch_oi_data(self, symbol):
        """Get OI data for symbol"""
    
    def fetch_fii_dii_data(self, date):
        """Get daily FII/DII data"""
    
    def _handle_rate_limit(self):
        """Wait if rate limited"""
```

**4. CacheManager**
```python
class CacheManager:
    def __init__(self, cache_dir='data/cache'):
        self.cache_dir = cache_dir
    
    def save(self, symbol, df):
        """Save data to cache"""
        # File format: cache/RELIANCE_NS.parquet or .csv
    
    def load(self, symbol):
        """Load data from cache"""
    
    def get_last_date(self, symbol):
        """Get last available date in cache"""
    
    def is_stale(self, symbol, max_age_hours=24):
        """Check if cache is outdated"""
```

---

## 5. Data Fetching Flow

### Morning Execution Flow

```
08:00 AM - START
    ↓
[1] Get Stock Universe
    ├── Load from cache (NIFTY_500_stocks.csv)
    ├── If cache > 7 days old, refresh from NSE
    └── Result: List of ~500 NIFTY 500 symbols
    ↓
[2] Fetch Price Data (OHLCV)
    ├── For each stock:
    │   ├── Check cache
    │   ├── Determine date range needed
    │   └── Fetch missing dates from yfinance
    ├── Use parallel processing (10-20 stocks at a time)
    ├── Handle failures (retry 3 times)
    └── Save to cache
    ↓
[3] Fetch OI Data (F&O stocks only)
    ├── Get list of F&O stocks (~200)
    ├── For each:
    │   ├── Scrape NSE option chain
    │   ├── Calculate OI change
    │   └── Calculate PCR
    ├── Rate limiting: 1 request per 3 seconds
    └── Save to cache
    ↓
[4] Fetch FII/DII Data
    ├── Scrape NSE FII/DII daily data
    ├── Match with individual stocks (sector mapping)
    ├── Calculate % change over 3 days
    └── Save to cache
    ↓
[5] Data Validation
    ├── Check for missing data
    ├── Check for outliers
    ├── Log any issues
    └── Mark problematic stocks
    ↓
08:30 AM - DATA READY for screening
```

---

## 6. Caching Strategy

### Cache Structure
```
data/
├── cache/
│   ├── price_data/
│   │   ├── RELIANCE.NS.parquet
│   │   ├── TCS.NS.parquet
│   │   └── ... (all stocks)
│   │
│   ├── oi_data/
│   │   ├── RELIANCE_OI.parquet
│   │   └── ... (F&O stocks)
│   │
│   ├── fii_dii/
│   │   ├── daily_fii_dii.parquet
│   │   └── stock_holdings.parquet
│   │
│   └── metadata/
│       ├── NSE_stocks.csv (stock universe)
│       ├── last_update.json (timestamp tracking)
│       └── failed_symbols.log
```

### Cache Rules
1. **Price Data:** Update daily, keep last 500 days
2. **OI Data:** Update daily, keep last 30 days
3. **FII/DII:** Update daily, keep last 90 days
4. **Stock Universe:** Update weekly

### File Format
- **Parquet** for large datasets (faster, compressed)
- **CSV** for small files (human-readable)
- **JSON** for metadata

---

## 7. Error Handling

### Common Errors & Solutions

**Error 1: Network timeout**
- **Solution:** Retry with exponential backoff (1s, 2s, 4s, 8s)
- **Max retries:** 3
- **Fallback:** Skip stock for this run, use cached data

**Error 2: NSE rate limiting (403/429)**
- **Solution:** 
  - Wait 60 seconds
  - Rotate user agents
  - Use session cookies
  - Reduce request frequency

**Error 3: Missing data for stock**
- **Solution:**
  - Try alternative symbol (RELIANCE.BO instead of .NS)
  - Check if stock is suspended
  - Mark as unavailable

**Error 4: Data quality issues**
- **Solution:**
  - Detect outliers (price change > 20% in one day = check)
  - Detect missing dates (gaps > 5 days = investigate)
  - Cross-validate with multiple sources

### Logging Strategy
```python
import logging

# Log everything
logger.info(f"Fetching {symbol} from {start} to {end}")
logger.warning(f"Cache miss for {symbol}")
logger.error(f"Failed to fetch {symbol}: {error}")

# Separate log files
- data_fetcher.log (general logs)
- errors.log (errors only)
- performance.log (timing metrics)
```

---

## 8. Performance Optimization

### Parallel Processing
```python
from concurrent.futures import ThreadPoolExecutor

def fetch_all_stocks(symbols):
    with ThreadPoolExecutor(max_workers=20) as executor:
        results = executor.map(fetch_single_stock, symbols)
    return results
```

**Optimal workers:** 10-20 (balance between speed and rate limits)

### Rate Limiting
```python
import time
from datetime import datetime

class RateLimiter:
    def __init__(self, max_requests_per_minute=60):
        self.max_requests = max_requests_per_minute
        self.requests = []
    
    def wait_if_needed(self):
        now = datetime.now()
        # Remove requests older than 1 minute
        self.requests = [r for r in self.requests 
                        if (now - r).seconds < 60]
        
        if len(self.requests) >= self.max_requests:
            sleep_time = 60 - (now - self.requests[0]).seconds
            time.sleep(sleep_time)
        
        self.requests.append(now)
```

### Expected Performance (NIFTY 500)
- **First run (full fetch):** 15-25 minutes for 500 stocks
- **Daily updates:** 3-5 minutes (only fetch yesterday's data)
- **Backtest data fetch:** 30-45 minutes for 2 years

---

## 9. Data Validation

### Validation Checks

**1. Completeness Check**
```python
def validate_completeness(df, expected_days=60):
    actual_days = len(df)
    missing_pct = (expected_days - actual_days) / expected_days
    
    if missing_pct > 0.1:  # More than 10% missing
        return False, f"Missing {missing_pct*100:.1f}% of data"
    return True, "OK"
```

**2. Data Quality Check**
```python
def validate_quality(df):
    # Check for zeros
    if (df['Close'] == 0).any():
        return False, "Zero prices detected"
    
    # Check for huge gaps
    pct_change = df['Close'].pct_change()
    if (abs(pct_change) > 0.5).any():  # 50% change
        return False, "Suspicious price movement"
    
    # Check for missing values
    if df.isnull().any().any():
        return False, "Missing values detected"
    
    return True, "OK"
```

**3. Date Continuity Check**
```python
def validate_dates(df):
    # Check for gaps in dates (excluding weekends)
    dates = pd.to_datetime(df.index)
    gaps = dates.diff()[1:]  # Skip first NaT
    
    # Max gap should be 3 days (weekend)
    if (gaps > pd.Timedelta(days=5)).any():
        return False, "Large gaps in dates"
    
    return True, "OK"
```

---

## 10. Configuration

**config/data_config.py:**
```python
# Data sources
YFINANCE_ENABLED = True
NSE_SCRAPING_ENABLED = True

# Lookback periods
DAILY_LOOKBACK_DAYS = 60
BACKTEST_LOOKBACK_DAYS = 500

# Cache settings
CACHE_DIR = 'data/cache'
CACHE_FORMAT = 'parquet'  # or 'csv'
MAX_CACHE_AGE_HOURS = 24

# Rate limiting
YFINANCE_BATCH_SIZE = 50
YFINANCE_DELAY_SECONDS = 1
NSE_REQUEST_DELAY_SECONDS = 3
MAX_RETRIES = 3

# Stock universe
NSE_STOCK_LIST_URL = 'https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20500'
UPDATE_STOCK_LIST_DAYS = 7

# Parallel processing
MAX_WORKERS = 20

# Validation
MAX_MISSING_DATA_PCT = 0.1  # 10%
MAX_SINGLE_DAY_CHANGE = 0.5  # 50%

# Logging
LOG_LEVEL = 'INFO'
LOG_FILE = 'logs/data_fetcher.log'
```

---

## 11. Usage Examples

### Example 1: Fetch data for daily screening
```python
from data_fetcher import DataFetcher

fetcher = DataFetcher()

# Fetch all NSE stocks (uses cache if available)
data = fetcher.fetch_for_screening(lookback_days=60)

# Returns dict: {symbol: DataFrame}
# DataFrame columns: Date, Open, High, Low, Close, Volume
```

### Example 2: Fetch for backtesting
```python
fetcher = DataFetcher()

data = fetcher.fetch_for_backtest(
    start_date='2024-01-01',
    end_date='2026-01-10',
    symbols=['RELIANCE.NS', 'TCS.NS', 'INFY.NS']
)
```

### Example 3: Fetch specific data types
```python
# Get only OI data
oi_data = fetcher.fetch_oi_data(symbols=['RELIANCE', 'TCS'])

# Get only FII/DII data
fii_dii = fetcher.fetch_fii_dii_data(days=5)

# Get stock universe
all_stocks = fetcher.get_stock_universe()
```

---

## 12. Testing Plan

**Unit Tests:**
- Test date range calculation
- Test cache save/load
- Test data validation
- Test error handling

**Integration Tests:**
- Test full fetch workflow
- Test with real API (sample stocks)
- Test cache invalidation
- Test parallel processing

**Performance Tests:**
- Measure fetch time for 100/500 stocks
- Measure cache hit rate
- Measure memory usage
- Verify all NIFTY 500 stocks fetched successfully

---

## Summary

**What:** Fetch OHLCV, OI, FII/DII data for NIFTY 500 stocks

**Stock Universe:** ~500 liquid, high-quality stocks (NIFTY 500 index)

**When:** Daily at 8:00 AM (incremental update)

**Where:** Yahoo Finance (price) + NSE website (OI, FII/DII)

**How Long:** 
- First run: 15-25 mins (500 stocks)
- Daily updates: 3-5 mins
- Backtest: 30-45 mins

**Cache:** Local parquet files, updated incrementally

**Reliability:** Retry logic, fallbacks, validation checks

**Benefits of NIFTY 500:**
✅ Liquid stocks = better execution
✅ Faster processing
✅ Better data quality
✅ Covers 95% of market cap
✅ Still plenty of trading opportunities

This data fetcher will be the foundation for the entire screening system!

