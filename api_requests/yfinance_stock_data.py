"""
yfinance API: Fetch OHLCV data for a stock
"""

import yfinance as yf
from datetime import datetime, timedelta


def get_stock_data(symbol, days=60, max_retries=2):
    """
    Fetch OHLCV data from yfinance for last N days
    
    Args:
        symbol (str): Stock symbol (e.g., 'RELIANCE.NS')
        days (int): Number of days to fetch (default: 60)
        max_retries (int): Number of retries if fetch fails (default: 2)
    
    Returns:
        DataFrame with Date, Open, High, Low, Close, Volume, Adj Close
    """
    
    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    # Format dates
    start = start_date.strftime('%Y-%m-%d')
    end = end_date.strftime('%Y-%m-%d')
    
    print(f"Fetching data for {symbol}")
    
    # Try multiple times if it fails
    for attempt in range(max_retries):
        try:
            # Download data
            data = yf.download(
                symbol,
                start=start,
                end=end,
                progress=False
            )
            
            if data.empty:
                print(f"  ⚠️  No data returned for {symbol}")
                if attempt < max_retries - 1:
                    print(f"  🔄 Retrying... (attempt {attempt + 2}/{max_retries})")
                    import time
                    time.sleep(1)
                    continue
                return None
            
            # Reset index to make Date a column
            data.reset_index(inplace=True)
            
            print(f"  ✅ Fetched {len(data)} days of data")
            return data
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
            if attempt < max_retries - 1:
                print(f"  🔄 Retrying... (attempt {attempt + 2}/{max_retries})")
                import time
                time.sleep(1)
                continue
            return None
    
    return None


# Alias for compatibility
def fetch_stock_data(symbol, days=60):
    """Alias for get_stock_data"""
    return get_stock_data(symbol, days)


if __name__ == "__main__":
    # Test with RELIANCE
    print("\n🧪 Testing yfinance API with RELIANCE.NS\n")
    
    df = get_stock_data('RELIANCE.NS', days=60)
    
    if df is not None:
        print("\n📊 Sample Data:")
        print(df.head())
        print(f"\n✅ Total rows: {len(df)}")
        print(f"✅ Columns: {list(df.columns)}")
    else:
        print("\n❌ Failed to fetch data")
