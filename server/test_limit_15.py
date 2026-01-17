"""
Test script to call /analyze API with limit=15
"""
import requests
import json
from datetime import datetime

def test_limit_15():
    """Test with limit=15"""
    url = "http://localhost:5000/analyze"
    payload = {"limit": 15}
    
    print("="*80)
    print(f"TEST: limit=15")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
    
    try:
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"\nStatus: {data.get('status')}")
            print(f"Message: {data.get('message')}")
            print(f"\nTop 15 Stocks:")
            print("-"*80)
            
            results = data.get('results', [])
            for idx, stock in enumerate(results):
                print(f"\n{idx + 1}. {stock['symbol']}")
                print(f"   Total Score: {stock['total_score']}")
                print(f"   Volume: {stock.get('volume_score', 'N/A')}")
                print(f"   MACD: {stock.get('macd_score', 'N/A')}")
                print(f"   RSI: {stock.get('rsi_score', 'N/A')}")
                print(f"   Trend/EMA: {stock.get('trend_ema_score', 'N/A')}")
                print(f"   ADX: {stock.get('adx_score', 'N/A')}")
                print(f"   OI Pattern: {stock.get('oi_pattern_score', 'N/A')}")
            
            print("\n" + "="*80)
            print(f"Total stocks returned: {len(results)}")
            print("="*80 + "\n")
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"Exception occurred: {str(e)}")

if __name__ == '__main__':
    test_limit_15()
