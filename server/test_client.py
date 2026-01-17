"""
Test client for the Stock Analysis API
"""
import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_health():
    """Test health endpoint"""
    print("\n" + "="*80)
    print("Testing /health endpoint...")
    print("="*80)
    
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_analyze(limit=10):
    """Test analyze endpoint"""
    print("\n" + "="*80)
    print(f"Testing /analyze endpoint with limit={limit}...")
    print("="*80)
    
    payload = {"limit": limit}
    
    response = requests.post(f"{BASE_URL}/analyze", json=payload)
    
    if response.status_code == 200:
        data = response.json()
        print(f"\nStatus: {data.get('status')}")
        print(f"Message: {data.get('message')}")
        
        results = data.get('results', [])
        if results:
            print(f"\nTop {len(results)} Stocks:")
            print("-"*80)
            for idx, stock in enumerate(results[:5]):  # Show top 5
                print(f"{idx+1}. {stock['symbol']} - Score: {stock['total_score']}")
            if len(results) > 5:
                print(f"... and {len(results) - 5} more stocks")
        else:
            print("\nNo results found")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

if __name__ == '__main__':
    # Test health endpoint
    if test_health():
        print("\n✓ Health check passed")
        
        # Test analyze endpoint
        test_analyze(limit=10)
    else:
        print("\n✗ Health check failed - is the server running?")
