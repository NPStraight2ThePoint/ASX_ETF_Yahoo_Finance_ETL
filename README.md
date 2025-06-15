# 📈 ASX ETF Data Pipeline (Yahoo Finance → PostgreSQL)

A simple ETL workflow to extract **Open, High, Low, Close, Volume (OHLCV)** data for all ASX-listed ETFs from Yahoo Finance and load it into a PostgreSQL database.

This pipeline supports both:
- Inception-to-date (ITD) historical data
- Daily incremental updates

---

## 🔄 Workflow Overview

1. **Extract ETF tickers** from [MarketIndex](https://www.marketindex.com.au/asx-etfs)
2. **Download OHLCV** data for each ticker from Yahoo Finance
3. **Fill missing values**
4. **Load into PostgreSQL** for long-term storage and analysis

---

## 📁 Files

| File | Description |
|------|-------------|
| `Market_Index_ASX_ETFs.xlsx` | Raw ETF descriptions from MarketIndex |
| `Market_Index_ASX_ETFs.csv` | Clean list of ETF tickers to loop through |

---

## 🧪 Scripts

| Script | Description |
|--------|-------------|
| `1_1_Get_ITD_OHLCV_ASX_ETFs.py` | Fetch inception-to-date OHLCV for all tickers |
| `2_1_Load_To_DB_ITD.py`        | Load ITD data into DB table `asx_etf_ohlcv` |
| `1_2_Daily_OHLCV_ASX_ETFs.py`  | Fetch daily OHLCV from last saved date |
| `2_2_Load_To_DB_Daily.py`      | Load daily data into DB table `asx_etf_ohlcv` |

---

## 🧱 Database

All data is stored in a PostgreSQL table:

```sql
CREATE TABLE asx_etf_ohlcv (
    ticker TEXT,
    date DATE,
    open FLOAT,
    high FLOAT,
    low FLOAT,
    close FLOAT,
    volume BIGINT,
    PRIMARY KEY (ticker, date)
);

