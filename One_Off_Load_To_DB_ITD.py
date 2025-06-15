import pandas as pd
from sqlalchemy import create_engine, MetaData
from sqlalchemy.dialects.postgresql import insert
from datetime import datetime
import os

today_str = datetime.today().strftime('%Y-%m-%d')
output_dir = r"C:\...\Pricing"
csv_path = os.path.join(output_dir, f"ASX_ETFs_OHLCV_{today_str}_ITD.csv")

db_url = "postgresql://postgres:...@localhost:5432/Yahoo_Finance_API"  # <-- replace
table_name = "asx_etf_ohlcv"

df = pd.read_csv(csv_path)
df.columns = df.columns.str.lower()
df['date'] = pd.to_datetime(df['date'])

engine = create_engine(db_url)
metadata = MetaData()
metadata.reflect(bind=engine)
table = metadata.tables[table_name]

records = df.to_dict(orient='records')
stmt = insert(table).values(records)
stmt = stmt.on_conflict_do_nothing(index_elements=['ticker', 'date'])

with engine.begin() as conn:
    conn.execute(stmt)

print("✅ Data inserted. Duplicates (ticker, date) automatically skipped.")




