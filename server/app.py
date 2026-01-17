"""
Flask API Server for Stock Analysis
Synchronous API that returns top N stocks directly
"""
from flask import Flask, request, jsonify
import sys
import os
import logging
from datetime import datetime

# Add parent directory to path to import main
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_requests.main import run_analysis_batched

app = Flask(__name__)

# Setup logging
log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
os.makedirs(log_dir, exist_ok=True)

log_file = os.path.join(log_dir, f'stock_analysis_{datetime.now().strftime("%Y%m%d")}.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Synchronous API endpoint to analyze stocks
    Request body: {"limit": 5}  (optional, defaults to 5)
    Returns: Top N stocks with scores directly
    """
    try:
        data = request.get_json() or {}
        limit = data.get('limit', 5)
        
        logging.info(f"Starting analysis for top {limit} stocks...")
        
        # Use batched processing only for large limits (>= 500 stocks)
        if limit >= 500:
            logging.info("Using batched processing (5 batches with 60s gaps)")
            results = run_analysis_batched(limit=5)  # Process all, return top 5
        else:
            logging.info(f"Processing first {limit} stocks")
            from api_requests.main import run_analysis
            results = run_analysis(limit=limit)  # Process 'limit' stocks, return top 5
        
        if not results:
            logging.warning("No results found")
            return jsonify({
                'status': 'completed',
                'message': 'No stocks found',
                'results': []
            }), 200
        
        logging.info(f"Analysis completed. Found {len(results)} stocks")
        
        return jsonify({
            'status': 'completed',
            'message': f'Found top {len(results)} stocks',
            'results': results
        }), 200
        
    except Exception as e:
        logging.error(f"Error in analyze endpoint: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    logging.info("Starting Flask server on port 5000...")
    app.run(debug=True, port=5000, host='0.0.0.0')
