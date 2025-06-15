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

| File | Description                                                       |
|------|-------------------------------------------------------------------|    
| `Market_Index_ASX_ETFs.xlsx` | Raw ETF descriptions from MarketIndex     |
| `Market_Index_ASX_ETFs.csv`  | Clean list of ETF tickers to loop through |

---

## 🧪 Scripts

| Script | Description                                                            |
|--------|------------------------------------------------------------------------|                                                      
| `1_1_Get_ITD_OHLCV_ASX_ETFs.py` | Fetch inception-to-date OHLCV for all tickers |
| `2_1_Load_To_DB_ITD.py`         | Load ITD data into DB table `asx_etf_ohlcv`   |
| `1_2_Daily_OHLCV_ASX_ETFs.py`   | Fetch daily OHLCV from last saved date        |
| `2_2_Load_To_DB_Daily.py`       | Load daily data into DB table `asx_etf_ohlcv` |

---

## 🧰 Tech Stack

- **Python 3.11+**
- **pandas** for data manipulation  
- **yfinance** for Yahoo Finance API access  
- **SQLAlchemy** + **psycopg2** for PostgreSQL database interaction  
- **PostgreSQL** for structured data storage 

## 🔗 Extends Into ML Pipeline

This ETL forms the **foundation** for a full ML-based investment pipeline.

➡️ The [ML Pipeline Repo]() includes:
- Linear price forecasting models  
- Portfolio optimisation using Sharpe Ratio maximisation  
- Realised vs Expected performance comparisons  
- Cleaned results stored in a separate PostgreSQL schema  

---

## 📌 Notes

- While this project is tailored for **ASX ETFs**, the workflow is fully adaptable to **any ticker list** supported by Yahoo Finance. Simply update the `CSV`/`Excel` input files.
- Designed to be modular and extendable — can support larger universes with minimal refactoring.

---

## 🚀 Future Additions

- Non-linear models for price forecasting  
- Volatility & factor models  
- Enhanced portfolio optimisation techniques



