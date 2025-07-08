import json
import yfinance as yf
import psycopg2

# Load tickers
with open("/app/tickers.json") as f:
    tickers_config = json.load(f)

# DB config
conn = psycopg2.connect(
    host="db",
    database="stocks",
    user="postgres",
    password="postgres"
)
cursor = conn.cursor()

for item in tickers_config:
    ticker = item["ticker"]
    company_name = item["company_name"]
    data = yf.Ticker(ticker).history(period="1d")
    if not data.empty:
        latest = data.iloc[-1]
        price = float(latest["Close"])
        volume = int(latest["Volume"])
        
        cursor.execute(
            \"""
            INSERT INTO stocks_import (ticker, company_name, price, volume)
            VALUES (%s, %s, %s, %s)
            \""",
            (ticker, company_name, price, volume)
        )
        print(f"Inserted: {ticker} | Price: {price} | Volume: {volume}")

conn.commit()
cursor.close()
conn.close()