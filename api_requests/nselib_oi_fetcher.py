"""
NSE Open Interest Data Fetcher using nselib
"""
import nselib
from nselib import derivatives
from datetime import datetime, timedelta

def get_oi_data(symbol, days=5):
    """
    Fetch Open Interest data for a symbol using nselib
    Returns OI pattern: 'long_buildup', 'short_covering', 'long_unwinding', 'short_buildup', or None
    
    Args:
        symbol: Stock symbol (without .NS suffix)
        days: Number of days of historical data to fetch
    """
    try:
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Format dates as DD-MM-YYYY
        start_date_str = start_date.strftime("%d-%m-%Y")
        end_date_str = end_date.strftime("%d-%m-%Y")
        
        # Fetch futures data
        data = derivatives.future_price_volume_data(
            symbol=symbol,
            instrument="FUTSTK",
            from_date=start_date_str,
            to_date=end_date_str
        )
        
        if data is None or data.empty:
            return None
        
        # Filter for nearest expiry futures contract only to ensure deterministic results
        # Parse EXPIRY_DT and get the nearest future expiry
        data['EXPIRY_DATE'] = data['EXPIRY_DT'].apply(
            lambda x: datetime.strptime(x, "%d-%b-%Y") if isinstance(x, str) else x
        )
        
        # Get current month's contract (nearest expiry in the future)
        current_date = datetime.now()
        future_expiries = data[data['EXPIRY_DATE'] >= current_date]
        
        if future_expiries.empty:
            # If no future expiries, take the most recent expired one
            nearest_expiry = data['EXPIRY_DATE'].max()
        else:
            # Take the nearest future expiry
            nearest_expiry = future_expiries['EXPIRY_DATE'].min()
        
        # Filter data for only this expiry
        data = data[data['EXPIRY_DATE'] == nearest_expiry].copy()
        
        if data.empty or len(data) < 2:
            return None
        
        # Sort by timestamp
        data = data.sort_values('TIMESTAMP')
        
        # Get latest and previous values
        latest = data.iloc[-1]
        previous = data.iloc[-2]
        
        # Calculate changes (using correct column names)
        price_change = latest['CLOSING_PRICE'] - previous['CLOSING_PRICE']
        oi_change = latest['OPEN_INT'] - previous['OPEN_INT']
        
        # Detect pattern
        pattern = detect_oi_pattern(price_change, oi_change)
        
        return pattern
    
    except KeyError as e:
        # Stock might not have F&O data
        print(f"ℹ️  No F&O data for {symbol}")
        return None
    except Exception as e:
        print(f"❌ Error fetching OI for {symbol}: {e}")
        return None

def detect_oi_pattern(price_change, oi_change):
    """
    Detect OI pattern based on price and OI changes
    """
    if price_change > 0 and oi_change > 0:
        return 'long_buildup'       # Bullish
    elif price_change > 0 and oi_change < 0:
        return 'short_covering'     # Bullish
    elif price_change < 0 and oi_change < 0:
        return 'long_unwinding'     # Bearish
    elif price_change < 0 and oi_change > 0:
        return 'short_buildup'      # Bearish
    else:
        return 'no_pattern'
