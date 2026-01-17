"""
Test script to fetch ASHOKLEY score from the API
"""
import requests
import json

def test_ashokley():
    """Test ASHOKLEY score by calling the analyze endpoint"""
    url = "http://localhost:5000/analyze"
    
    # Request with limit=500 to ensure ASHOKLEY is included
    payload = {"limit": 500}
    
    print("Sending request to analyze endpoint...")
    print(f"URL: {url}")
    print(f"Payload: {payload}")
    print("-" * 80)
    
    try:
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            
            # Find ASHOKLEY in results
            results = data.get('results', [])
            ashokley_found = False
            
            for idx, stock in enumerate(results):
                if stock['symbol'] == 'ASHOKLEY':
                    ashokley_found = True
                    print(f"\n{'='*80}")
                    print(f"ASHOKLEY FOUND - Rank: {idx + 1}")
                    print(f"{'='*80}")
                    print(f"Symbol: {stock['symbol']}")
                    print(f"Total Score: {stock['total_score']}")
                    print(f"\nDetailed Scores:")
                    print(f"  Volume Score: {stock.get('volume_score', 'N/A')}")
                    print(f"  MACD Score: {stock.get('macd_score', 'N/A')}")
                    print(f"  RSI Score: {stock.get('rsi_score', 'N/A')}")
                    print(f"  Trend/EMA Score: {stock.get('trend_ema_score', 'N/A')}")
                    print(f"  ADX Score: {stock.get('adx_score', 'N/A')}")
                    print(f"  OI Pattern Score: {stock.get('oi_pattern_score', 'N/A')}")
                    print(f"{'='*80}\n")
                    break
            
            if not ashokley_found:
                print("ASHOKLEY not found in results")
                print(f"Total stocks analyzed: {len(results)}")
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"Exception occurred: {str(e)}")

if __name__ == '__main__':
    test_ashokley()
