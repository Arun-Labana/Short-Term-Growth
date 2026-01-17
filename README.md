# Short-Term Growth Stock Analysis

A Python-based stock analysis tool that identifies short-term growth opportunities in NSE Nifty 500 stocks using technical indicators and scoring mechanisms.

## 🚀 Features

- **Real-time Stock Data Fetching**: Retrieves stock data from Yahoo Finance (yfinance)
- **Technical Indicators**:
  - RSI (Relative Strength Index)
  - MACD (Moving Average Convergence Divergence)
  - EMA 20 & EMA 50 (Exponential Moving Averages)
  - ADX (Average Directional Index)
  - Volume Analysis
- **Intelligent Scoring System**: Scores stocks based on multiple technical indicators
- **Flask API Server**: RESTful API to query stock recommendations
- **NSE Integration**: Supports all Nifty 500 stocks

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Arun-Labana/Short-Term-Growth.git
cd Short-Term-Growth
```

### 2. Create a Virtual Environment

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 📦 Dependencies

The project uses the following main libraries:
- `yfinance` - Yahoo Finance API for stock data
- `pandas` - Data manipulation and analysis
- `numpy` - Numerical computing
- `flask` - Web framework for API server
- `nselib` - NSE India data library
- Additional dependencies listed in `requirements.txt`

## 🏃 Usage

### Running the Analysis Script

To analyze stocks and get recommendations:

```bash
python api_requests/main.py
```

This will:
- Fetch the latest data for Nifty 500 stocks
- Calculate technical indicators
- Score each stock based on the indicators
- Display top recommendations

### Starting the Flask API Server

To start the API server:

```bash
cd server
python app.py
```

The server will start on `http://localhost:5000`

#### API Endpoints

**Get Top Stock Recommendations:**
```bash
# Get top 10 stocks
curl http://localhost:5000/api/stocks?limit=10

# Get specific stock analysis
curl http://localhost:5000/api/stocks/ASHOKLEY

# Get top 15 stocks
curl http://localhost:5000/api/stocks?limit=15
```

### Testing the API

Test files are available in the `server/` directory:

```bash
cd server

# Test with different limits
python test_limit_5.py
python test_limit_10.py
python test_limit_15.py

# Test specific stock
python test_ashokley.py
python test_ashokley_direct.py
```

## 📁 Project Structure

```
Short-Term-Growth/
├── api_requests/
│   ├── main.py                    # Main analysis script
│   ├── yfinance_stock_data.py     # Stock data fetcher
│   ├── nse_nifty500_list.py       # NSE Nifty 500 stock list
│   └── nselib_oi_fetcher.py       # Open Interest data fetcher
├── indicators/
│   ├── scorer.py                  # Scoring mechanism
│   └── yfinance_data/
│       ├── rsi.py                 # RSI indicator
│       ├── macd.py                # MACD indicator
│       ├── ema_20.py              # EMA 20 indicator
│       ├── ema_50.py              # EMA 50 indicator
│       ├── adx.py                 # ADX indicator
│       └── volume.py              # Volume analysis
├── config/
│   └── scoring_config.py          # Scoring configuration
├── server/
│   ├── app.py                     # Flask API server
│   └── test_*.py                  # Test scripts
├── logs/                          # Analysis logs
├── md files/                      # Documentation
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## ⚙️ Configuration

### Scoring Configuration

Modify `config/scoring_config.py` to adjust:
- Indicator weights
- RSI thresholds
- MACD parameters
- EMA crossover settings
- ADX strength levels
- Volume criteria

### Stock List

Update `api_requests/nse_nifty500_list.py` to:
- Add/remove stocks from analysis
- Modify stock universe
- Filter by market cap or sector

## 📊 Technical Indicators Explained

### RSI (Relative Strength Index)
- Measures momentum and overbought/oversold conditions
- Range: 0-100
- Buy signal: RSI < 30 (oversold)
- Sell signal: RSI > 70 (overbought)

### MACD (Moving Average Convergence Divergence)
- Trend-following momentum indicator
- Bullish: MACD line crosses above signal line
- Bearish: MACD line crosses below signal line

### EMA (Exponential Moving Average)
- EMA 20: Short-term trend
- EMA 50: Medium-term trend
- Bullish: Price above EMA & EMA 20 > EMA 50

### ADX (Average Directional Index)
- Measures trend strength
- ADX > 25: Strong trend
- ADX < 20: Weak or no trend

### Volume Analysis
- Compares current volume to average volume
- High volume confirms price movements

## 🔍 How It Works

1. **Data Collection**: Fetches historical stock data from Yahoo Finance
2. **Indicator Calculation**: Computes technical indicators for each stock
3. **Scoring**: Assigns scores based on indicator values and thresholds
4. **Ranking**: Ranks stocks by total score
5. **Output**: Returns top-ranked stocks with detailed metrics

## 📝 Logs

Analysis logs are stored in the `logs/` directory with timestamps:
- Format: `stock_analysis_YYYYMMDD.log`
- Contains: Execution details, errors, and analysis results

## 🤝 Contributing

Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## ⚠️ Disclaimer

This tool is for educational and research purposes only. It does not constitute financial advice. Always do your own research and consult with financial advisors before making investment decisions.

## 📧 Contact

**Author**: Arun Labana  
**Email**: labanaarun0@gmail.com  
**GitHub**: [@Arun-Labana](https://github.com/Arun-Labana)

## 📄 License

This project is open source and available for personal and educational use.

---

**Happy Trading! 📈**
