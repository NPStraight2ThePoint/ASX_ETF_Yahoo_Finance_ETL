Simple ETL workflow to extract ASX ETF Open,Close,High,Low,Volume for all ASX ETF tickers from yahoo finance API.

Fill N/A's and then load data in PostgreSQL DB.

Files : Market_Index_ASX_ETF's.xlsx    -> ASX ETF descriptions from marketindex  (https://www.marketindex.com.au/asx-etfs)
        Market_Index_ASX_ETFs.csv      -> List of tickers to loop through
        
Scripts : 1_1_Get_ITD_OHLCV_ASX_ETFs.py  -> Get inception to date OHLCV for all tickers
          2_1_Load_To_DB_ITD.py          -> Load inception to date OHLCV for all tickers into DB table 'asx_etf_ohlcv'
          1_2_Daily_OHLCV_ASX_ETFs.py    -> Get from last retreival date to date OHLCV for all tickers
          2_2_Load_To_DB_Daily.py        -> Load from last retreival date to date OHLCV for all tickers into DB table 'asx_etf_ohlcv'


This project will steadily grow to include:
         *linear & non linear price forecasts
         *portfolio optimisation
