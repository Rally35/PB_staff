import json
import yfinance as yf
import psycopg2
from datetime import datetime

# Load tickers
with open("tickers.json") as f:
    tickers_config = json.load(f)

# DB config
conn = psycopg2.connect(
    host="database",
    database="stocks",
    user="postgres",
    password="postgres"
)
cursor = conn.cursor()

# Truncate the import table before inserting new data
cursor.execute("TRUNCATE TABLE stocks_import")

for ticker in tickers_config:
    company_name = ticker
    data = yf.Ticker(ticker).history(period="1d")

    if not data.empty:
        latest = data.iloc[-1]
        price = round(float(latest["Close"]), 2)
        volume = int(latest["Volume"])
        date_str = latest.name.strftime("%Y-%m-%d")  # <-- Correct format for PostgreSQL DATE
        import_ts = datetime.utcnow()

        cursor.execute(
            """
            INSERT INTO stocks_import (ticker, company_name, price, volume, date, import_ts)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (ticker, company_name, price, volume, date_str, import_ts)
        )
        print(f"Inserted: {ticker} | Price: {price} | Volume: {volume} | Date: {date_str}")

conn.commit()
cursor.close()
conn.close()
