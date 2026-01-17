# NSE Website - Data to Fetch

## 1. NIFTY 500 Stock List
**URL:** `https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20500`

### Data Points:
1. symbol
2. open
3. dayHigh
4. dayLow
5. lastPrice
6. previousClose
7. totalTradedVolume
8. yearHigh
9. yearLow

### Frequency: Weekly

---

## 2. Open Interest Data (F&O stocks only)
**URL:** `https://www.nseindia.com/api/option-chain-equities?symbol=SYMBOL`

### Data Points:
1. strikePrice
2. CE openInterest (Call OI)
3. PE openInterest (Put OI)
4. CE changeinOpenInterest
5. PE changeinOpenInterest

### What We Calculate:
- Total Call OI
- Total Put OI
- PCR (Put-Call Ratio)
- OI Change %
- Pattern (Long buildup, Short covering, etc.)

### Days Required: **5 days**
- Need to compare today vs yesterday (minimum 2 days)
- Better to look at 3-5 day trend for confirmation
- Detect sustained buildup vs one-day spike

### Frequency: Daily

---

## 3. FII/DII Daily Market Activity
**URL:** `https://www.nseindia.com/api/fiidiiTrading`

### Data Points:
1. date
2. fii_buy_value
3. fii_sell_value
4. fii_net_value
5. dii_buy_value
6. dii_sell_value
7. dii_net_value

### Frequency: Daily

---

## 4. FII/DII Shareholding Pattern (Per Stock)
**URL:** `https://www.nseindia.com/api/corporates-shareholding?index=equities&symbol=SYMBOL`

### Data Points:
1. date (quarter end)
2. promoter_holding %
3. fii_holding %
4. dii_holding %
5. public_holding %
6. total_shares

### Days Required: **3-5 days**
- Compare today's FII/DII % vs 3 days ago
- Detect recent accumulation/distribution
- Short-term momentum indicator

### Frequency: Monthly check (data updates quarterly)

---

## Summary: Days Required

| Data Type | Days Needed | Why |
|-----------|-------------|-----|
| **OI Buildup** | 5 days | Compare today vs recent days, detect sustained patterns |
| **FII/DII Flow** | 3-5 days | Detect recent institutional accumulation trend |

**Total NSE data lookback:** 5 days (covers both indicators)

