"""
NSE API: Fetch NIFTY 500 Stock List
"""

import requests
import json


def get_nifty_500_stocks():
    """
    Fetch NIFTY 500 stock list from NSE
    
    Returns:
        list: List of dictionaries containing stock data
    """
    
    url = "https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20500"
    
    # NSE requires proper headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
    }
    
    # Create session to maintain cookies
    session = requests.Session()
    
    # First visit the main page to get cookies
    session.get('https://www.nseindia.com', headers=headers, timeout=10)
    
    # Now fetch the data
    response = session.get(url, headers=headers, timeout=10)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response Text (first 500 chars): {response.text[:500]}")
    
    if response.status_code == 200:
        try:
            data = response.json()
            stocks = data.get('data', [])
            
            # Extract only the fields we need
            stock_list = []
            for stock in stocks:
                stock_info = {
                    'symbol': stock.get('symbol'),
                    'open': stock.get('open'),
                    'dayHigh': stock.get('dayHigh'),
                    'dayLow': stock.get('dayLow'),
                    'lastPrice': stock.get('lastPrice'),
                    'previousClose': stock.get('previousClose'),
                    'totalTradedVolume': stock.get('totalTradedVolume'),
                    'yearHigh': stock.get('yearHigh'),
                    'yearLow': stock.get('yearLow'),
                }
                stock_list.append(stock_info)
            
            return stock_list
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse JSON: {e}")
    else:
        raise Exception(f"Failed to fetch data. Status code: {response.status_code}")


if __name__ == "__main__":
    # Test the API
    try:
        stocks = get_nifty_500_stocks()
        print(f"Successfully fetched {len(stocks)} stocks")
        print("\nFirst 3 stocks:")
        for i, stock in enumerate(stocks[:3]):
            print(f"\n{i+1}. {stock['symbol']}")
            print(f"   Last Price: {stock['lastPrice']}")
            print(f"   Volume: {stock['totalTradedVolume']}")
    except Exception as e:
        print(f"Error: {e}")

