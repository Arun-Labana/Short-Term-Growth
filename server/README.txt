Stock Analysis API Server
==========================

This Flask server provides a synchronous API to analyze stocks from NIFTY 500.

SETUP:
------
1. Make sure you're in the virtual environment:
   cd /Users/alabana/Documents/short-term-growth
   source venv/bin/activate

2. Install dependencies (if not already installed):
   pip install -r requirements.txt

STARTING THE SERVER:
-------------------
cd /Users/alabana/Documents/short-term-growth/server
source ../venv/bin/activate
python app.py

The server will start on http://localhost:5000

ENDPOINTS:
----------
1. Health Check
   GET /health
   Returns: {"status": "healthy"}

2. Analyze Stocks (Synchronous)
   POST /analyze
   Body: {"limit": 10}  (optional, defaults to 5)
   Returns: Top N stocks with scores directly

TESTING:
--------
1. Test health:
   curl http://localhost:5000/health

2. Test analysis (command line):
   curl -X POST http://localhost:5000/analyze \
     -H "Content-Type: application/json" \
     -d '{"limit": 10}'

3. Test using Python scripts:
   python test_client.py          # General test
   python test_ashokley.py        # Test specific stock (ASHOKLEY)
   python test_ashokley_direct.py # Direct calculation (no API)
   python test_limit_5.py         # Test with limit=5
   python test_limit_10.py        # Test with limit=10
   python test_limit_15.py        # Test with limit=15

LOGS:
-----
Logs are saved to: ../logs/stock_analysis_YYYYMMDD.log
Logs are also printed to console while server is running

STOPPING THE SERVER:
-------------------
Press Ctrl+C in the terminal where the server is running
