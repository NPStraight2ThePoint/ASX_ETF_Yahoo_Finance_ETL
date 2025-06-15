from sqlalchemy import create_engine, text
import pandas as pd
import yfinance as yf
import os
from datetime import datetime
from datetime import timedelta

db_url = "postgresql://postgres:...@localhost:5432/Yahoo_Finance_API"
engine = create_engine(db_url)
table_name = "asx_etf_ohlcv"
query = "SELECT date FROM asx_etf_ohlcv ORDER BY date DESC LIMIT 1;"

with engine.connect() as conn:
    result = conn.execute(text(query))
    latest_date = result.scalar()  # fetch single scalar value

print(f"Most recent price date in table: {latest_date}")

today_str = datetime.today().strftime('%Y-%m-%d')

tickers_df = pd.read_csv("Market_Index_ASX_ETFs.csv")

etf_tickers = tickers_df['ASX Code'].astype(str).str.upper()
etf_tickers = [ticker if ticker.endswith('.AX') else f"{ticker}.AX" for ticker in etf_tickers]

output_dir = r"C:\...\Pricing"
os.makedirs(output_dir, exist_ok=True)  # Ensure directory exists
output_filename = f"ASX_ETFs_OHLCV_{today_str}_Daily.csv"
output_filename_merged = f"ASX_ETFs_Merged_{today_str}_Daily.csv"
output_path = os.path.join(output_dir, output_filename)
output_path_merged = os.path.join(output_dir, output_filename_merged)

for ticker in etf_tickers:
    print(f"Fetching: {ticker}")
    try:
        #hist = yf.Ticker(ticker).history(period="max", interval="1d")
        hist = yf.Ticker(ticker).history(start=latest_date + timedelta(days=1), interval="1d")
        if not hist.empty:
            hist = hist.reset_index()
            hist['Date'] = hist['Date'].dt.tz_localize(None).dt.normalize()
            hist['Ticker'] = ticker
            hist = hist[['Ticker', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume']]

            # Write or append to CSV
            if not os.path.exists(output_path):
                hist.to_csv(output_path, index=False)
            else:
                hist.to_csv(output_path, mode='a', header=False, index=False)
    except Exception as e:
        print(f"Error fetching {ticker}: {e}")

print(f"Saved OHLCV data to: {output_path}")

df = pd.read_csv(output_path)
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df = df.dropna(subset=["Date"])
df["Date"] = df["Date"].dt.tz_localize(None).dt.normalize()
pivot_df = df.pivot(index="Date", columns="Ticker", values="Close")
pivot_df = pivot_df.sort_index().sort_index(axis=1)
pivot_df.to_csv(output_path_merged)

print("✅ Pivoted data saved to 'merged_ASX_ETFs_ITD.csv'")

df = pd.read_csv(output_path_merged)

df.columns = [col.lower() for col in df.columns]
df.rename(columns={df.columns[0]: 'date'}, inplace=True)
df['date'] = pd.to_datetime(df['date'], format='mixed', dayfirst=True, errors='coerce')
df = df.dropna(subset=['date'])
df = df.sort_values('date').reset_index(drop=True)
for col in df.columns[1:]:
    first_valid_idx = df[col].first_valid_index()
    if first_valid_idx is not None:
        df.loc[first_valid_idx:, col] = df.loc[first_valid_idx:, col].ffill()

df.to_csv(output_path_merged, index=False)
print("✅ Done. Missing prices filled after first observation.")

df = pd.read_csv(output_path, parse_dates=['Date'])
df.sort_values(by=['Ticker', 'Date'], inplace=True)
df[['Open', 'High', 'Low', 'Close', 'Volume']] = (
    df.groupby('Ticker')[['Open', 'High', 'Low', 'Close', 'Volume']].ffill()
)

df.to_csv(output_path, index=False)
